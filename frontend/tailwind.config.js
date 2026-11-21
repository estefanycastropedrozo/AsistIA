/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        teinco: {
          // Azul formal y pastel suave
          blue: '#1E40AF',           // Azul institucional formal
          blueDark: '#1E3A8A',       // Azul profundo
          blueSoft: '#EFF6FF',       // Azul pastel muy suave (fondos)
          blueBorder: '#BFDBFE',     // Borde azul pastel
          blueHover: '#DBEAFE',      // Hover azul pastel
          
          // Naranja pastel suave (no fosforescente, formal y cómodo a la vista)
          orange: '#D97706',         // Naranja ámbar formal
          orangeSoft: '#FFFBEB',     // Naranja pastel crema suave
          orangeBorder: '#FDE68A',   // Borde naranja pastel
          orangeHover: '#B45309',    // Naranja oscuro interactivo
          orangeAccent: '#EA580C',   // Acento naranja cálido
          
          // Fondos y neutros
          surface: '#F8FAFC',        // Fondo general descansado para la vista
          card: '#FFFFFF',           // Blanco puro para tarjetas
          text: '#0F172A',           // Texto legible
          muted: '#64748B',          // Texto secundario suave
        }
      }
    },
  },
  plugins: [],
}
