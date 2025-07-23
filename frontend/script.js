// File: frontend/script.js

document.getElementById("uploadForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const form = e.target;
  const file = form.file.files[0];
  const inputLanguage = form.input_language.value || "";
  const targetLanguage = form.target_language.value || "en";
  const diarize = form.diarize.checked;
  const customPrompt = form.custom_prompt.value;

  const formData = new FormData();
  formData.append("file", file);
  formData.append("input_language", inputLanguage);
  formData.append("target_language", targetLanguage);
  formData.append("diarize", diarize);
  formData.append("custom_prompt", customPrompt);

  document.getElementById("output").textContent = "Processing... Please wait...";

  try {
    const response = await fetch("https://concisio-v2.onrender.com/process", {
      method: "POST",
      body: formData
    });

    if (!response.ok) {
      throw new Error("Server returned an error");
    }

    const data = await response.json();
    document.getElementById("output").innerHTML = `
      <h3>Transcript</h3>
      <div>${data.transcript}</div>
      <h3>Translated</h3>
      <div>${data.translated}</div>
      <h3>Summary</h3>
      <div>${data.summary}</div>
    `;
  } catch (err) {
    document.getElementById("output").textContent = "Error: " + err.message;
  }
});
