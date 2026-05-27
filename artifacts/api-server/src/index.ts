import app from "./app";
import { logger } from "./lib/logger";

const isVercel = !!process.env.VERCEL;

if (!isVercel) {
  const port = Number(process.env.PORT || 3000);

  app.listen(port, () => {
    logger.info({ port }, "Server running locally");
  });
}

export default app;
