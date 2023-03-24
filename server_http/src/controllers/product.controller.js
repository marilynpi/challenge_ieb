import pool from '../db.js'
import * as dotenv from 'dotenv'

dotenv.config()

const getProducts = async (req, res, next) => {
  try {
    const result = await pool.query('SELECT * FROM ' + process.env.DB_TABLE)
    console.log(result.rows)
    res.send(result.rows)
  } catch (error) {
    next(error)
  }
}

const getProduct = async (req, res, next) => {
  try {
    const { id } = req.params
    const result = await pool.query('SELECT * FROM ' + process.env.DB_TABLE + ' WHERE id = $1', [id])
    if (result.rows.length === 0) {
      return res.status(404).json({
        message: 'Product not found'
      })
    }
    console.log(result.rows[0])
    res.send(result.rows[0])
  } catch (error) {
    next(error)
  }
}

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
