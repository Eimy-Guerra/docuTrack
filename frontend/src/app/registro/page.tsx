'use client'

import { useState } from "react"

export default function RegistroPage() {
  const [nombre, setNombre] = useState("")
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [loading, setLoading] = useState(false)

  const handleRegistro = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)

    try {
      const response = await fetch("http://localhost:8000/registro/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ nombre, email, password })
      })

      const data = await response.json()
      setLoading(false)

      if (response.ok && data.access_token && data.rol) {
      localStorage.setItem("token", data.access_token)
      localStorage.setItem("rol", data.rol)
      window.location.href = "/seguimiento"
      }else {
        alert(data.detail || "Error al registrar")
      }
    } catch {
      setLoading(false)
      alert("Error de conexión con el backend")
    }
  }

  const regresar = () => {
    window.location.href = "/login"
  }

  return (
    <div className="min-h-screen flex justify-center items-center bg-gray-50 p-6">
      <form onSubmit={handleRegistro} className="bg-white p-8 rounded shadow-md w-full max-w-md">
        <h2 className="text-2xl font-bold mb-6 text-center text-green-700">Registro de Usuario</h2>

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
          className="w-full p-2 mb-4 border rounded"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />

        <button
          type="submit"
          disabled={loading}
          className="w-full bg-green-600 text-white py-2 rounded hover:bg-green-700"
        >
          {loading ? "Registrando..." : "Registrarse"}
        </button>

        {/* ✅ Botón de regreso agregado aquí */}
        <button
          type="button"
          onClick={regresar}
          className="w-full mt-3 bg-blue-500 text-white py-2 rounded hover:bg-blue-600"
        >
          ← Regresar al Login
        </button>

        <p className="text-center text-sm mt-4 text-gray-500">
          Ya tienes cuenta? Inicia sesión para acceder al sistema.
        </p>
      </form>
    </div>
  )
}
