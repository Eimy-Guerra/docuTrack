'use client'

import { useState } from "react"

export default function RegistroPage() {
  const [nombre, setNombre] = useState("")
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()

    try {
      const response = await fetch("http://localhost:8000/users/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          nombre,
          correo: email,
          contraseña: password,
          rol: "cliente"  // Rol fijo para evitar registro como admin
        })
      })

      const data = await response.json()

      if (response.ok) {
        alert("¡Registro exitoso! Puedes iniciar sesión ahora")
      } else {
        alert(data.detail || "Error al registrar usuario")
      }

    } catch (error) {
      alert("Error de conexión con el backend")
    }
  }

  return (
    <div className="min-h-screen flex justify-center items-center bg-gray-100">
      <form className="bg-white p-8 rounded shadow-md w-full max-w-md" onSubmit={handleSubmit}>
        <h2 className="text-xl font-bold mb-6 text-center">Registro de Usuario</h2>

        <label className="block mb-2">Nombre completo:</label>
        <input
          type="text"
          className="w-full p-2 mb-4 border rounded"
          value={nombre}
          onChange={(e) => setNombre(e.target.value)}
          required
        />

        <label className="block mb-2">Email:</label>
        <input
          type="email"
          className="w-full p-2 mb-4 border rounded"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />

        <label className="block mb-2">Contraseña:</label>
        <input
          type="password"
          className="w-full p-2 mb-6 border rounded"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />

        <button type="submit" className="w-full bg-green-600 text-white py-2 rounded hover:bg-green-700">
          Registrarse
        </button>
      </form>
    </div>
  )
}
