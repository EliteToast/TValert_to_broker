module.exports = (req, res) => {
    if (req.method === 'GET') {
        res.json("Vercel API by TerminalTom")
    }
}