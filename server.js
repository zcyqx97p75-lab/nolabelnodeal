import express from "express";

const app = express();

// Hauptdomain für die Weiterleitung
const TARGET = "https://www.no-label-no-deal.eu";

app.use((req, res) => {
  const url = TARGET + req.originalUrl;
  res.redirect(301, url);
});

const port = process.env.PORT || 3000;
app.listen(port, () => {
  console.log(`Redirector listening on ${port}`);
});
