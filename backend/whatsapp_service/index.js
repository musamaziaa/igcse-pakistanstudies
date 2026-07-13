const { default: makeWASocket, useMultiFileAuthState, DisconnectReason } = require("@whiskeysockets/baileys");
const pino = require("pino");
const qrcode = require("qrcode-terminal");
const express = require("express");
const bodyParser = require("body-parser");
const path = require("path");

const app = express();
app.use(bodyParser.json());

let sock = null;
let connectionStatus = "connecting";

async function connectToWhatsApp() {
  const { state, saveCreds } = await useMultiFileAuthState(path.join(__dirname, "auth_info_baileys"));
  
  sock = makeWASocket({
    auth: state,
    printQRInTerminal: false, // We will print it custom with qrcode-terminal to control layout
    logger: pino({ level: "silent" })
  });

  sock.ev.on("creds.update", saveCreds);

  sock.ev.on("connection.update", (update) => {
    const { connection, lastDisconnect, qr } = update;
    if (qr) {
      console.log("\n📲 SCAN THIS QR CODE WITH WHATSAPP TO CONNECT:\n");
      qrcode.generate(qr, { small: true });
    }

    if (connection === "close") {
      const shouldReconnect = lastDisconnect?.error?.output?.statusCode !== DisconnectReason.loggedOut;
      console.log("Connection closed due to ", lastDisconnect?.error, ", reconnecting: ", shouldReconnect);
      connectionStatus = "disconnected";
      if (shouldReconnect) {
        connectToWhatsApp();
      }
    } else if (connection === "open") {
      console.log("✅ WHATSAPP CONNECTION OPENED SUCCESSFULLY!");
      connectionStatus = "connected";
    }
  });
}

// REST API endpoint to send a message
app.post("/send-message", async (req, res) => {
  const { phone, message } = req.body;
  if (!phone || !message) {
    return res.status(400).json({ error: "Missing phone or message in request body" });
  }

  if (connectionStatus !== "connected" || !sock) {
    return res.status(503).json({ error: "WhatsApp service is not connected yet" });
  }

  try {
    // Format phone number to WhatsApp JID format (e.g. 923001234567@s.whatsapp.net)
    // Strip non-numeric characters
    let cleanPhone = phone.replace(/\D/g, "");
    if (!cleanPhone.endsWith("@s.whatsapp.net")) {
      cleanPhone = `${cleanPhone}@s.whatsapp.net`;
    }

    await sock.sendMessage(cleanPhone, { text: message });
    console.log(`✉️ Message sent to ${cleanPhone}`);
    return res.json({ success: true });
  } catch (error) {
    console.error("Failed to send message:", error);
    return res.status(500).json({ error: error.message });
  }
});

// Endpoint to check status
app.get("/status", (req, res) => {
  res.json({ status: connectionStatus });
});

// Start the express server
const PORT = process.env.PORT || 3001;
app.listen(PORT, () => {
  console.log(`🚀 WhatsApp microservice listening on port ${PORT}`);
});

// Initiate connection
connectToWhatsApp();
