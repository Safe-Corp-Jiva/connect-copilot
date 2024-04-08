async function readStream(apiUrl) {
  try {
    const response = await fetch(apiUrl, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ "input": "Multiply 30 and 20", "chat_history": [] })
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const reader = response.body.getReader();
    const decoder = new TextDecoder();

    while (true) {
      const { done, value } = await reader.read();
      if (done) {
        break;
      }
      const text = decoder.decode(value);
      try {
        const obj = JSON.parse(text);
        if (obj.output) {
          process.stdout.write(obj.output?.result ?? obj.output);
        } else if (obj.action) {
          process.stdout.write(`Running \`${obj.action}\`...\n`);
        }
      } catch (error) {
        console.error("Failed to parse json");
      }
    }

    console.log("Response Finished.");
  } catch (error) {
    console.error(error);
  }
}
