import pg from 'pg'
import * as dotenv from 'dotenv'

// Load environment variables
dotenv.config({ path: '../.env' })

const { Pool } = pg

// Connect to DataBase and create a Pool
const pool = new Pool({
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
  host: process.env.DB_HOST,
  port: process.env.DB_PORT,
  database: process.env.DB_DATABASE
})

export default pool
