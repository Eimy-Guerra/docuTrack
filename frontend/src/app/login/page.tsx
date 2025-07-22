'use client'

import { useState } from "react"

export default function LoginPage() {
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [loading, setLoading] = useState(false)

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)

    try {
      const response = await fetch("http://localhost:8000/token/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ correo: email, contraseña: password })
      })

      const data = await response.json()
      setLoading(false)

      if (response.ok && data.access_token && data.rol) {
        localStorage.setItem("token", data.access_token)
        localStorage.setItem("rol", data.rol)

        if (data.rol === "admin") {
          window.location.href = "/admin"
        } else {
          window.location.href = "/seguimiento"
        }
      } else {
        alert(data.detail || "Credenciales incorrectas")
      }
    } catch {
      setLoading(false)
      alert("Error de conexión con el backend")
    }
  }

  return (
    <div className="min-h-screen flex flex-col justify-center items-center bg-gray-50 p-6">
      <form onSubmit={handleLogin} className="bg-white p-8 rounded shadow-md w-full max-w-md">
        <h2 className="text-2xl font-bold mb-6 text-center text-blue-700">Inicio de Sesión</h2>

        <label className="block mb-2">Correo electrónico:</label>
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
          className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700"
        >
          {loading ? "Ingresando..." : "Iniciar Sesión"}
        </button>

        <p className="text-center text-sm mt-4 text-gray-500">
          Accede como cliente o administrador según tus credenciales.
        </p>
      </form>

      <button
        onClick={() => (window.location.href = "/registro")}
        className="mt-4 text-blue-600 hover:underline text-sm"
      >
        ¿No tienes cuenta? Regístrate aquí
      </button>
    </div>
  )
}
