import Router from 'express'
import { getProducts, getProduct, updateProduct } from '../controllers/product.controller.js'


/**
 * Creates Router and defines endpoints and his behaviors
*/

const router = Router()

router.get('/', (req, res) => {
  res.send('REST API')
})

router.get('/products', getProducts)
router.get('/product/:id', getProduct)
router.put('/product/:id', updateProduct)

export default router
