import express, { type Express } from "express";
import cors from "cors";
import router from "./routes";
import { logger } from "./lib/logger";
const pinoHttp = require("pino-http");
const app: Express = express();
const loggerMiddleware = pinoHttp({
  logger,
  serializers: {
    req(req: any) {
      return {
        id: req.id,
        method: req.method,
        url: req.url?.split("?")[0],
      };
    },
    res(res: any) {
      return {
        statusCode: res.statusCode,
      };
    },
  },
});
export default app;
