'use client'

import { useState } from "react"

export default function SolicitudPage() {
  const [nombre, setNombre] = useState("")
  const [apellido, setApellido] = useState("")
  const [tipo, setTipo] = useState("nacimiento")
  const [cursaActualmente, setCursaActualmente] = useState(false)
  const [fechaFin, setFechaFin] = useState("")
  const [fechaInicio, setFechaInicio] = useState("")
  const [fechaNacimiento, setFechaNacimiento] = useState("")
  const [lugarNacimiento, setLugarNacimiento] = useState("")
  const [cedulaArchivo, setCedulaArchivo] = useState<File | null>(null)
  const [lugarEstudios, setLugarEstudios] = useState("")

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    const token = localStorage.getItem("token")
    if (!token) {
      alert("Usuario no autenticado")
      return
    }

    const formData = new FormData()
    formData.append("nombre_usuario", nombre)
    formData.append("apellido_usuario", apellido)
    formData.append("tipo", tipo)

    if (tipo === "estudios") {
      formData.append("lugar_estudio", lugarEstudios)
      formData.append("fecha_inicio_estudios", fechaInicio)
      formData.append("cursa_actualmente", JSON.stringify(cursaActualmente))
      if (!cursaActualmente && fechaFin) {
        formData.append("fecha_fin_estudios", fechaFin)
      }
    }

    if (tipo === "nacimiento") {
      formData.append("fecha_nacimiento", fechaNacimiento)
      formData.append("lugar_nacimiento", lugarNacimiento)
    }

    if (cedulaArchivo) {
      formData.append("cedula_archivo", cedulaArchivo)
    }

    try {
      const response = await fetch("http://localhost:8000/requests/", {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`
        },
        body: formData
      })

      const data = await response.json()
      if (response.ok) {
        alert("Solicitud creada con éxito 🎉")
      } else {
        alert(data.detail || "Error al crear la solicitud")
      }
    } catch (err) {
      alert("Error de conexión con el backend")
    }
  }

  const cerrarSesion = () => {
    localStorage.removeItem("token")
    alert("Sesión cerrada")
    window.location.href = "/login"
  }

  return (
    <div className="min-h-screen flex justify-center items-center bg-gray-50 p-4">
      <form className="bg-white p-8 rounded shadow-md w-full max-w-md" onSubmit={handleSubmit}>
        <h2 className="text-xl font-bold mb-6 text-center">Solicitud de Certificado</h2>

        <label className="block mb-2">Nombre:</label>
        <input
          type="text"
          className="w-full p-2 mb-4 border rounded"
          value={nombre}
          onChange={(e) => setNombre(e.target.value)}
          required
        />

        <label className="block mb-2">Apellido:</label>
        <input
          type="text"
          className="w-full p-2 mb-4 border rounded"
          value={apellido}
          onChange={(e) => setApellido(e.target.value)}
          required
        />

        <label className="block mb-2">Tipo de certificado:</label>
        <select
          className="w-full p-2 mb-4 border rounded"
          value={tipo}
          onChange={(e) => setTipo(e.target.value)}
        >
          <option value="nacimiento">Nacimiento</option>
          <option value="estudios">Estudios</option>
        </select>

        {tipo === "estudios" && (
          <>
            <label className="block mb-2">Lugar de estudios:</label>
            <input
              type="text"
              className="w-full p-2 mb-4 border rounded"
              value={lugarEstudios}
              onChange={(e) => setLugarEstudios(e.target.value)}
              required
            />

            <label className="block mb-2">Fecha de inicio de estudios:</label>
            <input
              type="date"
              className="w-full p-2 mb-4 border rounded"
              value={fechaInicio}
              onChange={(e) => setFechaInicio(e.target.value)}
              required
            />

            <label className="flex items-center mb-2">
              <input
                type="checkbox"
                checked={cursaActualmente}
                onChange={(e) => setCursaActualmente(e.target.checked)}
                className="mr-2"
              />
              ¿Actualmente cursa?
            </label>

            {!cursaActualmente && (
              <>
                <label className="block mb-2">Fecha de finalización de estudios:</label>
                <input
                  type="date"
                  className="w-full p-2 mb-4 border rounded"
                  value={fechaFin}
                  onChange={(e) => setFechaFin(e.target.value)}
                />
              </>
            )}
          </>
        )}

        {tipo === "nacimiento" && (
          <>
            <label className="block mb-2">Fecha de nacimiento:</label>
            <input
              type="date"
              className="w-full p-2 mb-4 border rounded"
              value={fechaNacimiento}
              onChange={(e) => setFechaNacimiento(e.target.value)}
              required
            />

            <label className="block mb-2">Lugar de nacimiento:</label>
            <input
              type="text"
              className="w-full p-2 mb-4 border rounded"
              value={lugarNacimiento}
              onChange={(e) => setLugarNacimiento(e.target.value)}
              required
            />
          </>
        )}

        <label className="block mb-2 font-medium text-gray-700">
          Imagen de tu Cédula (PDF o JPG):
        </label>
        <input
          type="file"
          accept=".pdf,.jpg,.jpeg"
          className="w-full mb-6 px-4 py-2 border-2 border-blue-500 bg-blue-50 text-sm text-gray-700 rounded cursor-pointer file:bg-blue-600 file:text-white file:px-4 file:py-2 file:rounded file:border-none file:cursor-pointer"
          onChange={(e) => setCedulaArchivo(e.target.files?.[0] || null)}
          required
        />

        <button type="submit" className="w-full bg-green-600 text-white py-2 rounded hover:bg-green-700">
          Enviar Solicitud
        </button>

        <p className="text-sm text-center mt-4">
          ¿Ya realizaste una solicitud?{" "}
          <a href="/seguimiento" className="text-blue-600 hover:underline">
            Ver estado aquí
          </a>
        </p>

        <p className="text-sm text-center mt-2">
          <button onClick={cerrarSesion} className="text-red-600 hover:underline">
            Cerrar sesión
          </button>
        </p>
      </form>
    </div>
  )
}
