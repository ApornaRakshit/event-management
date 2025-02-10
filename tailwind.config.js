/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html",
    "./**/templates/**/*.html"
  ],
  theme: {
    extend: {},
  },
//   plugins: [],
// }
plugins: [
  require('daisyui'),
],
}
