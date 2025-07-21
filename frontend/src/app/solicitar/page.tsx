'use client'

import { useState } from "react"

export default function SolicitudPage() {
  const [nombre, setNombre] = useState("")
  const [tipo, setTipo] = useState("nacimiento")
  const [archivo, setArchivo] = useState<File | null>(null)
  const [cursaActualmente, setCursaActualmente] = useState(false)
  const [fechaFin, setFechaFin] = useState("")

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    const token = localStorage.getItem("token")
    if (!token) {
      alert("Usuario no autenticado")
      return
    }

    const formData = new FormData()
    formData.append("nombre", nombre)
    formData.append("tipo_certificado", tipo)
    formData.append("cursa_actualmente", JSON.stringify(cursaActualmente))
    if (!cursaActualmente && fechaFin) {
      formData.append("fecha_fin_estudios", fechaFin)
    }
    if (archivo) {
      formData.append("archivo", archivo)
    }

    try {
      const response = await fetch("http://localhost:8000/solicitudes", {
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

  return (
    <div className="min-h-screen flex justify-center items-center bg-gray-50">
      <form className="bg-white p-8 rounded shadow-md w-full max-w-md" onSubmit={handleSubmit}>
        <h2 className="text-xl font-bold mb-6 text-center">Solicitud de Certificado</h2>

        <label className="block mb-2">Nombre completo:</label>
        <input
          type="text"
          className="w-full p-2 mb-4 border rounded"
          value={nombre}
          onChange={(e) => setNombre(e.target.value)}
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

        <label className="block mb-2">Archivo adjunto (PDF o JPG):</label>
        <input
          type="file"
          accept=".pdf,.jpg,.jpeg"
          className="w-full mb-6"
          onChange={(e) => setArchivo(e.target.files?.[0] || null)}
        />

        <button type="submit" className="w-full bg-green-600 text-white py-2 rounded hover:bg-green-700">
          Enviar Solicitud
        </button>
      </form>
    </div>
  )
}
