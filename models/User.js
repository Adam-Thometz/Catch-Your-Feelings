const db = require('../db')
const ExpressError = require('../expressError')
const bcrypt = require('bcrypt')
const { BCRYPT_WORK_FACTOR, SECRET_KEY } = require('../config')
const jwt = require('jsonwebtoken')

class User {
  static async register({username, password, email}) {
    if (!username || !password || !email) {
      throw new ExpressError('You must provide all info', 400)
    }

    const hashedPw = await bcrypt.hash(password, BCRYPT_WORK_FACTOR)
    const results = await db.query(`
      INSERT INTO users (username, password, email)
      VALUES ($1, $2, $3)
      RETURNING username, password, email`,
      [username, hashedPw, email])
    return results.rows[0]
  }

  static async authenticate(username, password) {
    if (!username || !password) throw new ExpressError('You must provide a username and a password', 400)
    const results = await db.query(`
      SELECT password
      FROM users
      WHERE username = $1`,
    [username])
    const user = results.rows[0]
    return user && await bcrypt.compare(password, user.password)
  }
}