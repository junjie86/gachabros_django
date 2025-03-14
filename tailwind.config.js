/** @type {import('tailwindcss').Config} */
module.exports = {
    content: ['./templates/**/*.html', './**/templates/**/*.html', './**/*.js', './**/*.py'],
    darkMode: 'class',
    theme: {
        extend: {
            aspectRatio: {
                '4/3': '4 / 3',
            },
        },
    },
    plugins: [require('@tailwindcss/aspect-ratio')],
};
