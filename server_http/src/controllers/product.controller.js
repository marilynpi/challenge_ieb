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
 * @summary Updates product prices by ID received as URI parameter, acording with a JSON received as request body.
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

/**
 * Gets a random integer number between min and max.
 * @param {integer} min: min value (excluded)
 * @param {integer} max: max value (included)
 * @return {integer} random integer between min and max
 */
const randomInt = (min, max) => {
  return Math.floor(Math.random() * (max - min + 1)) + min;
}

/**
 * Gets a random item from a array: sort array randomly and return first item
 * @param list {array} array to get the random item
 * @return {array} random integer between min and max
 */
const getRandomItem = (list) => {
  list.sort(function() {return 0.5 - Math.random()}) // random number between -0.5 and 0.49999
  return list[0]
}

/**
 * Updates prices for a product random with random values
 */
const updateProductRandomly = async() => {
  try {
    const result = await pool.query('SELECT * FROM ' + process.env.DB_TABLE)

    // get random product
    const ramdomProduct = getRandomItem(result.rows)
    let { id, purchaseprice, saleprice } = ramdomProduct

    // update prices ramdomly between -5 and 5
    purchaseprice = purchaseprice + randomInt(-6, 5)
    saleprice = saleprice + randomInt(-6, 5)

    try {
      const result = await pool.query('UPDATE ' + process.env.DB_TABLE + ' SET purchasePrice = $1, salePrice = $2 WHERE id=$3 returning *', [
        purchaseprice,
        saleprice,
        id
      ])

      console.log('Product prices updated successfully')
      console.log('Product ID: ' + id)
      console.log('New prices: ' + purchaseprice + ', ' + saleprice )
  
      if (result.rowCount === 0) {
        console.log ('Product not found')
      }  
    } catch (error) {
      console.log (error)
    }
  } catch (error) {
    console.log (error)
  }
}

/**
 * Updates prices for products random with random values in a time interval
 * @param time {number} time in milliseconds
 */
const updateProductsInterval = (time) => {
  updateProductRandomly()
  setInterval(async() =>
  {
    updateProductRandomly()
  }, time)
}

export { getProducts, getProduct, updateProduct, updateProductsInterval }
