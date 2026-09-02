// WebAssembly for the calculator app

package main

import (
	"fmt"
	"math"
	"strconv"
	"strings"
	"syscall/js"
)

// ---- Tokenizer ----

type tokenKind int

const (
	tokNumber tokenKind = iota
	tokPlus
	tokMinus
	tokStar
	tokSlash
	tokLParen
	tokRParen
	tokIdent
	tokEOF
)

type token struct {
	kind  tokenKind
	num   float64
	ident string
}

type lexer struct {
	input []rune
	pos   int
}

func newLexer(s string) *lexer {
	return &lexer{input: []rune(s), pos: 0}
}

func (l *lexer) peekRune() rune {
	if l.pos >= len(l.input) {
		return 0
	}
	return l.input[l.pos]
}

func (l *lexer) next() (token, error) {
	// skip whitespace
	for l.pos < len(l.input) && (l.input[l.pos] == ' ' || l.input[l.pos] == '\t') {
		l.pos++
	}
	if l.pos >= len(l.input) {
		return token{kind: tokEOF}, nil
	}

	c := l.input[l.pos]

	switch c {
	case '+':
		l.pos++
		return token{kind: tokPlus}, nil
	case '-':
		l.pos++
		return token{kind: tokMinus}, nil
	case '*':
		l.pos++
		return token{kind: tokStar}, nil
	case '/':
		l.pos++
		return token{kind: tokSlash}, nil
	case '(':
		l.pos++
		return token{kind: tokLParen}, nil
	case ')':
		l.pos++
		return token{kind: tokRParen}, nil
	}

	if isDigit(c) || c == '.' {
		start := l.pos
		seenDot := false
		for l.pos < len(l.input) && (isDigit(l.input[l.pos]) || l.input[l.pos] == '.') {
			if l.input[l.pos] == '.' {
				if seenDot {
					return token{}, fmt.Errorf("unexpected extra '.' in number")
				}
				seenDot = true
			}
			l.pos++
		}
		numStr := string(l.input[start:l.pos])
		val, err := strconv.ParseFloat(numStr, 64)
		if err != nil {
			return token{}, fmt.Errorf("invalid number: %s", numStr)
		}
		return token{kind: tokNumber, num: val}, nil
	}

	if isLetter(c) {
		start := l.pos
		for l.pos < len(l.input) && isLetter(l.input[l.pos]) {
			l.pos++
		}
		name := string(l.input[start:l.pos])
		return token{kind: tokIdent, ident: name}, nil
	}

	return token{}, fmt.Errorf("unexpected character: %q", string(c))
}

func isDigit(c rune) bool {
	return c >= '0' && c <= '9'
}

func isLetter(c rune) bool {
	return (c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z')
}

// ---- Recursive-descent parser / evaluator ----
//
// Grammar:
//   expr    := term (( '+' | '-' ) term)*
//   term    := unary (( '*' | '/' ) unary)*
//   unary   := '-' unary | primary
//   primary := NUMBER | '(' expr ')' | IDENT '(' expr ')'
//
// IDENT is a function name: sin, cos, tan, ln, exp (all take one argument).

type parser struct {
	lex *lexer
	cur token
}

func newParser(input string) (*parser, error) {
	lex := newLexer(input)
	p := &parser{lex: lex}
	if err := p.advance(); err != nil {
		return nil, err
	}
	return p, nil
}

func (p *parser) advance() error {
	t, err := p.lex.next()
	if err != nil {
		return err
	}
	p.cur = t
	return nil
}

func (p *parser) parseExpr() (float64, error) {
	val, err := p.parseTerm()
	if err != nil {
		return 0, err
	}
	for p.cur.kind == tokPlus || p.cur.kind == tokMinus {
		op := p.cur.kind
		if err := p.advance(); err != nil {
			return 0, err
		}
		rhs, err := p.parseTerm()
		if err != nil {
			return 0, err
		}
		if op == tokPlus {
			val += rhs
		} else {
			val -= rhs
		}
	}
	return val, nil
}

func (p *parser) parseTerm() (float64, error) {
	val, err := p.parseUnary()
	if err != nil {
		return 0, err
	}
	for p.cur.kind == tokStar || p.cur.kind == tokSlash {
		op := p.cur.kind
		if err := p.advance(); err != nil {
			return 0, err
		}
		rhs, err := p.parseUnary()
		if err != nil {
			return 0, err
		}
		if op == tokStar {
			val *= rhs
		} else {
			if rhs == 0 {
				return 0, fmt.Errorf("division by zero")
			}
			val /= rhs
		}
	}
	return val, nil
}

func (p *parser) parseUnary() (float64, error) {
	if p.cur.kind == tokMinus {
		if err := p.advance(); err != nil {
			return 0, err
		}
		val, err := p.parseUnary()
		if err != nil {
			return 0, err
		}
		return -val, nil
	}
	if p.cur.kind == tokPlus {
		if err := p.advance(); err != nil {
			return 0, err
		}
		return p.parseUnary()
	}
	return p.parsePrimary()
}

func (p *parser) parsePrimary() (float64, error) {
	switch p.cur.kind {
	case tokNumber:
		val := p.cur.num
		if err := p.advance(); err != nil {
			return 0, err
		}
		return val, nil
	case tokLParen:
		if err := p.advance(); err != nil {
			return 0, err
		}
		val, err := p.parseExpr()
		if err != nil {
			return 0, err
		}
		if p.cur.kind != tokRParen {
			return 0, fmt.Errorf("expected ')'")
		}
		if err := p.advance(); err != nil {
			return 0, err
		}
		return val, nil
	case tokIdent:
		name := p.cur.ident
		if err := p.advance(); err != nil {
			return 0, err
		}
		if p.cur.kind != tokLParen {
			return 0, fmt.Errorf("expected '(' after %s", name)
		}
		if err := p.advance(); err != nil {
			return 0, err
		}
		arg, err := p.parseExpr()
		if err != nil {
			return 0, err
		}
		if p.cur.kind != tokRParen {
			return 0, fmt.Errorf("expected ')' after %s argument", name)
		}
		if err := p.advance(); err != nil {
			return 0, err
		}
		return applyFunction(name, arg)
	default:
		return 0, fmt.Errorf("unexpected token in expression")
	}
}

// applyFunction evaluates a named single-argument function. Angles for
// trig functions are in radians.
func applyFunction(name string, arg float64) (float64, error) {
	switch strings.ToLower(name) {
	case "sin":
		return math.Sin(arg), nil
	case "cos":
		return math.Cos(arg), nil
	case "tan":
		return math.Tan(arg), nil
	case "ln":
		if arg <= 0 {
			return 0, fmt.Errorf("ln undefined for non-positive values")
		}
		return math.Log(arg), nil
	case "exp":
		return math.Exp(arg), nil
	default:
		return 0, fmt.Errorf("unknown function: %s", name)
	}
}

// evaluateExpr parses and evaluates a full expression string, ensuring
// the entire input is consumed (catches trailing garbage / mismatched parens).
func evaluateExpr(input string) (float64, error) {
	input = strings.TrimSpace(input)
	if input == "" {
		return 0, fmt.Errorf("empty expression")
	}
	p, err := newParser(input)
	if err != nil {
		return 0, err
	}
	val, err := p.parseExpr()
	if err != nil {
		return 0, err
	}
	if p.cur.kind != tokEOF {
		return 0, fmt.Errorf("unexpected trailing input")
	}
	return val, nil
}

// ---- JS-exported entry point ----

func evaluate(this js.Value, args []js.Value) interface{} {
	if len(args) < 1 {
		return errorJSON("no expression provided")
	}
	expr := args[0].String()

	val, err := evaluateExpr(expr)
	if err != nil {
		return errorJSON(err.Error())
	}
	return successJSON(val)
}

func successJSON(val float64) string {
	return fmt.Sprintf(`{"result":%s}`, strconv.FormatFloat(val, 'g', -1, 64))
}

func errorJSON(msg string) string {
	return fmt.Sprintf(`{"error":%q}`, msg)
}

func main() {
	c := make(chan struct{}, 0)
	js.Global().Set("evaluate", js.FuncOf(evaluate))
	fmt.Println("Calculator WASM module ready")
	<-c
}
