import express from 'express'
import router from './routes/product.routes.js'
import * as dotenv from 'dotenv'

dotenv.config({ path: '../.env' })

const app = express()
const port = process.env.REST_API_PORT

app.use(express.json())
app.use(router)

app.listen(port, () => {
  console.log(`Server on port ${port}`)
})
