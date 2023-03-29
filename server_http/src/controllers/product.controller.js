import pool from '../db.js'
import * as dotenv from 'dotenv'

// Load environment variables
dotenv.config({ path: '../../.env' })

/**
 * GET /products
 * @summary Gets all products 
 * @tags products
 * @return {object} 200 - success response - application/json
 * @return {object} 400 - Bad request response
 */
const getProducts = async (req, res, next) => {
  try {
    const result = await pool.query('SELECT * FROM ' + process.env.DB_TABLE)
    res.send(result.rows)
  } catch (error) {
    next(error)
  }
}

/**
 * GET /product/{id}:
 * @summary Gets a product by id
 * @tags products
 * @return {object} 200 - success response - application/json
 * @return {object} 400 - Bad request response
 */
const getProduct = async (req, res, next) => {
  try {
    const { id } = req.params
    const result = await pool.query('SELECT * FROM ' + process.env.DB_TABLE + ' WHERE id = $1', [id])
    if (result.rows.length === 0) {
      return res.status(404).json({
        message: 'Product not found'
      })
    }
    res.send(result.rows[0])
  } catch (error) {
    next(error)
  }
}

/**
 * PUT /product/{id}:
 * Request body example:
 * {
 *   "purchasePrice": 300,
 *   "salePrice": 304
 * }
 * @summary Updates a product prices by ID and acording with a JSON received as URI parameter and a JSON received as request body.
 * @tags products
 * @return {object} 200 - success response - application/json
 * @return {object} 400 - Bad request response
 */
const updateProduct = async (req, res, next) => {
  try {
    const { id } = req.params
    const { purchasePrice, salePrice } = req.body

    if (!purchasePrice || !salePrice) throw new Error('Parameters empty')

    const result = await pool.query('UPDATE ' + process.env.DB_TABLE + ' SET purchasePrice = $1, salePrice = $2 WHERE id=$3 returning *', [
      purchasePrice,
      salePrice,
      id
    ])

    if (result.rowCount === 0) {
      return res.status(404).json({
        message: 'Product not found'
      })
    }

    return res.sendStatus(204)
  } catch (error) {
    next(error)
  }
}

export { getProducts, getProduct, updateProduct }
