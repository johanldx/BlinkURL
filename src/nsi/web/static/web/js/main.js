const textAnim = document.querySelector('#typewriter');

new Typewriter(textAnim, {
    loop: true,
    deleteSpeed: 20
})
.typeString('étudiants')
.pauseFor(3000)
.deleteChars(9)
.typeString('musiciens')
.pauseFor(3000)
.deleteChars(9)
.typeString('professeurs')
.pauseFor(3000)
.deleteChars(11)
.typeString('créateurs')
.pauseFor(3000)
.deleteChars(9)
.start()