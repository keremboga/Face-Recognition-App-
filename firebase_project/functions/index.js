const functions = require("firebase-functions");
const admin = require("firebase-admin");
const axios = require("axios");

// Firestore ve Storage istemcilerini başlatın
admin.initializeApp();
const db = admin.firestore();

exports.handleFirestoreEvent = functions.firestore
    .document("identities/{documentId}")
    .onCreate(async (snap, context) => {
      const newValue = snap.data();
      const image = newValue.image;
      const id = newValue.id;

      const docRef = db.collection("identities").doc(context.params.documentId);

      // Aynı id'ye sahip diğer belgeleri kontrol et
      const snapshot = await db
          .collection("identities")
          .where("id", "==", id)
          .get();

      if (snapshot.size === 1) {
      // İlk belge
        await docRef.update({
          verified: true,
          initial_request: true,
          status: "DONE",
        });
      } else {
      // Aynı id'ye sahip diğer belgeler mevcut
        await docRef.update({
          status: "WAITING",
        });

        try {
        // Python servisine istek gönder
          const response = await axios.post(
              "https://new-service-y5czgx732q-uc.a.run.app/verify",
              {
                image: image,
                id: id,
              },
          );

          const result = response.data;

          await docRef.update({
            verified: result.verified,
            status: "DONE",
            initial_request: false,
          });
        } catch (error) {
          console.error("Error sending request to Python service:", error);
          await docRef.update({
            status: "ERROR",
            initial_request: false,
          });
        }
      }
    });
