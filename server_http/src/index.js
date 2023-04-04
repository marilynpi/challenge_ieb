import express from 'express'
import router from './routes/product.routes.js'
import * as dotenv from 'dotenv'

// Load environment variables
dotenv.config({ path: '../.env' })

const app = express()
const port = (process.env.REST_API_PORT) ? process.env.REST_API_PORT : '3000'
const host = (process.env.REST_API_HOST) ? process.env.REST_API_HOST : 'localhost'

// Needed to express read json objects
app.use(express.json())
app.use(router)

// Start http server
app.listen(port, host, () => {
  console.log(`Server on  ${host}:${port}`)
  console.log(`GET products: ${host}:${port}/products`)
  console.log(`GET a product: ${host}:${port}/product/:id`)
  console.log(`PUT a product: ${host}:${port}/product/:id`)
  
})
