const http = require("http");

const TARGET = "https://www.no-label-no-deal.eu";

const server = http.createServer((req, res) => {
  if (req.url === "/healthz") {
    res.statusCode = 200;
    res.end("ok");
    return;
  }

  const location = TARGET + req.url;
  res.statusCode = 301;
  res.setHeader("Location", location);
  res.setHeader("Cache-Control", "public, max-age=300");
  res.end();
});

const port = process.env.PORT || 3000;
server.listen(port, () => {
  console.log(`Redirector listening on ${port}`);
});
