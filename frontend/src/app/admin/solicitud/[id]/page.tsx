'use client'

import { useState, useEffect } from 'react'
import { useParams } from 'next/navigation'

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
  documento_url?: string
}

const estadosTraducidos: { [key: string]: string } = {
  pendiente: "Recibido",
  en_validacion: "En Validación",
  correccion: "Para Corrección",
  aprobado: "Emitido",
  rechazado: "Rechazado"
}

export default function SolicitudDetalle() {
  const params = useParams()
  const id = params?.id
  const [solicitud, setSolicitud] = useState<Solicitud | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const token = localStorage.getItem("token")
    if (!token) {
      alert("No estás autenticado")
      window.location.href = "/login"
      return
    }

    fetch(`http://localhost:8000/requests/${id}`, {
      headers: { Authorization: `Bearer ${token}` }
    })
      .then(res => res.json())
      .then(data => {
        setSolicitud(data)
        setLoading(false)
      })
      .catch(() => {
        alert("Error al cargar solicitud")
        setLoading(false)
      })
  }, [id])

  const realizarAccion = async (accion: string) => {
    const token = localStorage.getItem("token")
    if (!token) return alert("No estás autenticado")

    try {
      const res = await fetch(`http://localhost:8000/requests/${id}/${accion}`, {
        method: "PUT",
        headers: { Authorization: `Bearer ${token}` }
      })

      const data = await res.json()
      if (res.ok) {
        alert(`✅ Solicitud ${accion} con éxito`)
        window.location.href = "/admin"
      } else {
        alert(data.detail || `Error al ejecutar ${accion}`)
      }
    } catch {
      alert("Error al conectar con el backend")
    }
  }

  if (loading) return <p className="p-8 text-center">Cargando solicitud...</p>
  if (!solicitud) return <p className="p-8 text-center text-red-600">Solicitud no encontrada</p>

  const esEstudios = solicitud.tipo.toLowerCase().includes("estudio")
  const estadoActual = solicitud.estado

  return (
    <div className="min-h-screen bg-gray-50 p-8 max-w-2xl mx-auto">
      <h1 className="text-3xl font-bold text-center text-blue-700 mb-6">
        📝 Revisión de Solicitud #{solicitud.id}
      </h1>

      <div className="bg-white p-6 rounded shadow-md space-y-3 border-l-4 border-blue-600">
        <p><strong>Solicitante:</strong> {solicitud.nombre_usuario} {solicitud.apellido_usuario}</p>
        <p><strong>Tipo de certificado:</strong> {esEstudios ? "Estudios" : "Nacimiento"}</p>
        <p><strong>Estado actual:</strong> <span className="text-green-700 font-medium">
          {estadosTraducidos[estadoActual] || estadoActual}
        </span></p>

        {esEstudios ? (
          <>
            <p><strong>Lugar de estudios:</strong> {solicitud.lugar_estudio || "No especificado"}</p>
            <p><strong>Inicio:</strong> {solicitud.fecha_inicio_estudios}</p>
            <p><strong>Fin:</strong> {solicitud.fecha_fin_estudios || "Actualmente cursando"}</p>
          </>
        ) : (
          <p><strong>Fecha de nacimiento:</strong> {solicitud.fecha_nacimiento}</p>
        )}

        {solicitud.documento_url && (
          <div className="mt-4">
            <p className="font-semibold">📄 Documento enviado:</p>
            <a
              href={`http://localhost:8000/${solicitud.documento_url}`}
              target="_blank"
              rel="noopener noreferrer"
              className="text-blue-600 underline"
            >
              Ver documento
            </a>
          </div>
        )}
      </div>

      {/* ✅ Mostrar acciones si el estado es tratable */}
      {["pendiente", "en_validacion", "correccion"].includes(estadoActual) && (
        <div className="mt-6 flex justify-center space-x-4">
          <button
            onClick={() => realizarAccion("corregir")}
            className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
          >
            Solicitar Corrección
          </button>
          <button
            onClick={() => realizarAccion("rechazar")}
            className="bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600"
          >
            Rechazar
          </button>
          <button
            onClick={() => realizarAccion("aprobar")}
            className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700"
          >
            Aprobar
          </button>
        </div>
      )}

      <div className="mt-8 text-center">
        <a href="/admin" className="text-blue-600 font-medium hover:underline">
          ← Volver al dashboard
        </a>
      </div>
    </div>
  )
}
