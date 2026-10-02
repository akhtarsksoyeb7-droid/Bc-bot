const express = require('express');
const app = express();
const PORT = process.env.PORT || 3000;

app.get('/', (req, res) => {
  res.send('Bc-bot is Live!');
});

app.listen(PORT, () => {
  console.log('Running on ' + PORT);
});
