import express from 'express';
import http from 'http';
import { Server } from 'socket.io';
import bodyParser from 'body-parser';

const app = express();
const server = http.createServer(app);
const io = new Server(server);

const port = 3000;

// Define the interface for a single tile
interface Tile {
  icon: string;
  tile_type: string;
  building?: string;
  key?: string;
  owners: string[];
  height: number;
}

// Define the interface for the entire map data
type MapData = Tile[][];

// Middleware
app.use(bodyParser.json());

// Routes
app.get('/', (req, res) => {
  res.send('Hello, World!');
});

// Socket.IO
io.on('connection', socket => {
  console.log('A user connected:', socket.id);

  socket.on('disconnect', () => {
    console.log('A user disconnected:', socket.id);
  });

  socket.on('map_data', data => {
    setTimeout(() => {
      console.log('waited 3 seconds');
      console.log(data);
      io.emit('updated_map_data', { data });
    }, 3000);
  });
});

// Start Server
server.listen(port, () => {
  console.log(`Server is running on http://0.0.0.0:${port}`);
});
