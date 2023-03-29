import express from 'express'
import router from './routes/product.routes.js'
import * as dotenv from 'dotenv'

// Load environment variables
dotenv.config({ path: '../.env' })

const app = express()
const port = process.env.REST_API_PORT

// Needed to express read json objects
app.use(express.json())
app.use(router)

// Start http server
app.listen(port, () => {
  console.log(`Server on port ${port}`)
})
