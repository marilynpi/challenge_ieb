import express from 'express'
import router from './routes/product.routes.js'

const app = express()
const port = 4000

app.use(express.json())
app.use(router)

app.listen(port, () => {
  console.log(`Server on port ${port}`)
})
