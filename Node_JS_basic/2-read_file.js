const fs = require('fs');

function countStudents(path) {
  try {
    // Lire le fichier CSV
    const data = fs.readFileSync(path, 'utf8');
    const lines = data.split('\n').filter(line => line.trim() !== ''); // Filtrer les lignes vides

    if (lines.length === 0) {
      throw new Error('Cannot load the database');
    }

    // Enlever la première ligne qui contient les en-têtes
    const headers = lines.shift().split(',');
    const fieldIndex = headers.indexOf('field'); // Trouver l'index du champ 'field'

    const studentsByField = {};

    lines.forEach((line) => {
      const studentData = line.split(',');
      const field = studentData[fieldIndex];
      const firstName = studentData[0]; // On suppose que le prénom est dans la première colonne

      if (field) {
        if (!studentsByField[field]) {
          studentsByField[field] = [];
        }
        studentsByField[field].push(firstName);
      }
    });

    // Compte le nombre total d'étudiants
    const totalStudents = lines.length;
    console.log(`Number of students: ${totalStudents}`);

    // Affiche le nombre detudiant
    for (const field in studentsByField) {
      const students = studentsByField[field];
      console.log(`Number of students in ${field}: ${students.length}. List: ${students.join(', ')}`);
    }
  } catch (error) {
    throw new Error('Cannot load the database');
  }
}

module.exports = countStudents;

