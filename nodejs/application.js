import express from 'express';
import http from 'http';
import * as routes from './routes/routeIndex.js';

console.log("API Booting up!");

var stateFarmClaimsServer = express();


stateFarmClaimsServer.use('/agents', routes.agentRoutes());
stateFarmClaimsServer.use('/disaster', routes.disasterRoutes());
stateFarmClaimsServer.use('/claims', routes.claimRoutes());
stateFarmClaimsServer.use('/states', routes.stateRoutes());




var server = http.createServer(stateFarmClaimsServer)
var port = 443// use env file later process.env.PORT
server.listen(port, ()=>{
    console.log('server running at port '+port);
});