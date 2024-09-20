// 1-stdin.js

console.log("Welcome to Holberton School, what is your name?");

process.stdin.on('data', (data) => {
    const name = data.toString().trim();
    console.log(`Your name is: ${name}`);

    // Fermeture du programme
    process.stdin.pause(); // Arret de lecture

    console.log("This important software is now closing");
});
