'use client'

import { useEffect, useState } from "react"

type Solicitud = {
  id: number
  tipo: string
  estado: string
  nombre_usuario: string
  apellido_usuario: string
  fecha_nacimiento?: string
  lugar_estudio?: string
  fecha_inicio_estudios?: string
  fecha_fin_estudios?: string
}

const estadosTraducidos: { [key: string]: string } = {
  pendiente: "Recibido",
  en_validacion: "En Validación",
  correccion: "Para Corrección",
  aprobado: "Emitido",
  rechazado: "Rechazado"
}

export default function SeguimientoPage() {
  const [solicitudes, setSolicitudes] = useState<Solicitud[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const token = localStorage.getItem("token")
    if (!token) return alert("Usuario no autenticado")

    fetch("http://localhost:8000/mis-requests/", {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })
      .then(res => res.json())
      .then(data => {
        if (!Array.isArray(data)) {
          alert(data.detail || "Error al obtener solicitudes")
          setLoading(false)
          return
        }
        setSolicitudes(data)
        setLoading(false)
      })
      .catch(() => {
        alert("Error de conexión con el backend")
        setLoading(false)
      })
  }, [])

  const descargarCertificado = async (id: number) => {
    const token = localStorage.getItem("token")
    if (!token) return alert("No estás autenticada")

    try {
      const res = await fetch(`http://localhost:8000/requests/${id}/certificado`, {
        headers: {
          Authorization: `Bearer ${token}`
        }
      })

      if (!res.ok) {
        const error = await res.json()
        alert(error.detail || "No se pudo descargar el certificado")
        return
      }

      const blob = await res.blob()
      const url = window.URL.createObjectURL(blob)
      const link = document.createElement("a")
      link.href = url
      link.download = "certificado.pdf"
      link.click()
      window.URL.revokeObjectURL(url)
    } catch {
      alert("Error al conectar con el servidor")
    }
  }

  return (
    <div className="min-h-screen bg-gray-100 p-6">
      <h1 className="text-3xl font-bold text-center mb-6 text-blue-700">
        📍 Seguimiento de tus Solicitudes
      </h1>

      {loading && <p className="text-center">Cargando solicitudes...</p>}

      {!loading && solicitudes.length === 0 && (
        <p className="text-center text-gray-600">
          No has realizado ninguna solicitud aún.
        </p>
      )}

      <div className="grid gap-6 max-w-3xl mx-auto">
        {solicitudes.map((solicitud) => {
          const tipoNormalizado = String(solicitud.tipo || "").toLowerCase().trim()
          const esEstudios = tipoNormalizado.includes("estudio")

          return (
            <div
              key={solicitud.id}
              className="bg-white shadow-md rounded p-6 border-l-4 border-blue-600"
            >
              <h2 className="text-xl font-semibold text-blue-800 mb-2">
                Certificado de {esEstudios ? "Estudios" : "Nacimiento"}
              </h2>

              <p><strong>Nombre:</strong> {solicitud.nombre_usuario} {solicitud.apellido_usuario}</p>
              <p>
                <strong>Estado actual:</strong>{" "}
                <span className="text-green-700 font-medium">
                  {estadosTraducidos[solicitud.estado] || solicitud.estado}
                </span>
              </p>

              {esEstudios && (
                <>
                  <p><strong>Lugar de estudios:</strong> {solicitud.lugar_estudio || "No especificado"}</p>
                  <p><strong>Inicio:</strong> {solicitud.fecha_inicio_estudios}</p>
                  <p><strong>Fin:</strong> {solicitud.fecha_fin_estudios || "Actualmente cursando"}</p>
                </>
              )}

              {!esEstudios && (
                <p><strong>Fecha de nacimiento:</strong> {solicitud.fecha_nacimiento}</p>
              )}

              {solicitud.estado === "aprobado" && (
                <div className="mt-4">
                  <p className="font-semibold text-gray-800">📥 Certificado disponible:</p>
                  <button
                    onClick={() => descargarCertificado(solicitud.id)}
                    className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700 mt-2"
                  >
                    Descargar PDF
                  </button>
                </div>
              )}
            </div>
          )
        })}
      </div>

      <div className="mt-8 text-center">
        <a href="/solicitar" className="text-blue-600 font-medium hover:underline">
          ← Regresar a solicitud de certificado
        </a>
      </div>
    </div>
  )
}
