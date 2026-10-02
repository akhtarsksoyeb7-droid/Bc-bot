const express = require('express');
const app = express();
const PORT = process.env.PORT || 3000;

app.get('/', (req, res) => {
  res.send('Bc-bot is Running!');
});

app.listen(PORT, () => {
  console.log('Bot running on port ' + PORT);
});
