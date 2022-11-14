const obfuscated = document.getElementsByClassName("obfuscated-email");
for (const cur of obfuscated) {
    const email = cur.dataset.email.split("").map(c => String.fromCharCode(c.charCodeAt(0) ^ 1)).join("");
    cur.href = "mailto:" + email;
    cur.innerText = email;
}
