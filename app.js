const express = require("express");
const nunjucks = require("nunjucks");
const bodyParser = require('body-parser');
const routes = require('./routes');
const ExpressError = require("./expressError");

const app = express();

app.use(express.urlencoded({ extended: true }));
app.use(express.static(__dirname + '/public'));

nunjucks.configure("templates", {
  autoescape: true,
  express: app
});

app.use(routes)

/** 404 handler */

app.use(function(req, res, next) {
  const err = new ExpressError("Page not Found");
  err.status = 404;

  // pass the error to the next piece of middleware
  return next(err);
});

/** general error handler */

app.use((err, req, res, next) => {
  res.status(err.status || 500);

  return res.render("error.html", { err });
});

module.exports = app;
