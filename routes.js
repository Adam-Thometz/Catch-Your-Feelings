const express = require("express");
const router = new express.Router();

/** Landing page */

router.get("/", function(req, res, next) {
  return res.render("index.html");
});

/** The feelings catcher */

router.get("/about", function(req, res, next) {
  return res.render("about.html");
});

/** User routes */

module.exports = router