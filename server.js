/** Start server for Catch Your Feelings */
const PORT = process.env.PORT || 3000

const app = require("./app");

app.listen(PORT, function() {
  console.log(`listening on ${PORT}`);
});