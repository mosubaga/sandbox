const doescontentmatch = require('./browser');

jest.setTimeout(30000);

test('Sample Text', async () => {
    const sAnswer = await doescontentmatch();
    await expect(sAnswer).toBeFalsy();
});