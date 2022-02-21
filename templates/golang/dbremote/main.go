package main

import (
    "context"
    "net"
    "flag"
    "golang.org/x/crypto/ssh"
    "database/sql"
    "github.com/go-sql-driver/mysql"
    "log"
    "os"
    "fmt"
    "strings"
)

var host string
var port string
var user string
var command string
var password string

type ViaSSHDialer struct {
    client *ssh.Client
}

func (self *ViaSSHDialer) Dial(_ context.Context,addr string) (net.Conn, error) {
    return self.client.Dial("tcp", addr)
}

func init() {
    flag.StringVar(&host, "host", "", "SSH hostname or IP")
    flag.StringVar(&port, "port", "", "SSH port")
    flag.StringVar(&user, "user", "", "SSH user")
    // flag.StringVar(&command, "command", "", "Command to execute on server")
    flag.StringVar(&password, "password", "", "Password to get to the server")
    flag.Parse()
    if host == "" || port == "" || user == "" || password == "" {
        flag.PrintDefaults()
        os.Exit(2)
    }
}

func main() {
    conf := &ssh.ClientConfig{
        User: user,
        Auth: []ssh.AuthMethod{
            ssh.Password(password),
        },
        HostKeyCallback: ssh.InsecureIgnoreHostKey(), // XXX: Security issue - Ignore 
    }
    client, err := ssh.Dial("tcp", strings.Join([]string{host, ":", port}, ""), conf)
    mustExec(err, "failed to dial SSH server")
    session, err := client.NewSession()
    mustExec(err, "failed to create SSH session")
    defer session.Close()

    dbUser := "[dbuser]"         // DB username
    dbPass := "[dbpassword]"         // DB Password
    dbHost := "localhost:3306" // DB Hostname/IP
    dbName := "[dbname]"       // Database name

    // Now we register the ViaSSHDialer with the ssh connection as a parameter
    // mysql.RegisterDial("mysql+tcp", (&ViaSSHDialer{client}).Dial) < -- depcrecated
    mysql.RegisterDialContext("mysql+tcp", (&ViaSSHDialer{client}).Dial)

    // And now we can use our new driver with the regular mysql connection string tunneled through the SSH connection
    if db, err := sql.Open("mysql", fmt.Sprintf("%s:%s@mysql+tcp(%s)/%s", dbUser, dbPass, dbHost, dbName)); err == nil {

    fmt.Printf("Successfully connected to the db\n")

    if rows, err := db.Query("SELECT text,out FROM table_name"); err == nil {
        for rows.Next() {
            var text string
            var name string
            rows.Scan(&text,&name)
            fmt.Printf("tkey: %s, pkey: %s\n",text,name)
        }
        rows.Close()
    } else {
        fmt.Printf("Failure: %s", err.Error())
    }

    db.Close()

    } else {
      fmt.Printf("Failed to connect to the db: %s\n", err.Error())
    }

    // Try some ssh command to test...
    // var b bytes.Buffer
    // session.Stdout = &b
    // err = session.Run(command)
    // mustExec(err, "failed to run command over SSH")
    // log.Printf("%s:\n%s", command, b.String())

}

func mustExec(err error, msg string) {
    if err != nil {
        log.Fatalf("%s:\n  %s", msg, err)
    }
}
