let savedData = null;

module.exports = (req, res) => {
  if (req.method === 'GET') {
    if (savedData !== null) {
      res.json(savedData);
    } else {
      res.status(404).json({ error: 'No data available' });
    }
  } else if (req.method === 'POST') {
    const body = req.body;
    if (!body) {
      res.status(400).json({ error: 'Invalid data' });
      return;
    }
    savedData = body;
    res.json(savedData);
  }
};
