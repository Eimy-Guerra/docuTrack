'use client'

import { useEffect, useState } from 'react'
import { useParams } from 'next/navigation'

type Solicitud = {
  id: number
  tipo: string
  estado: string
  nombre_usuario: string
  apellido_usuario: string
  documento_url?: string
}

const estadosTraducidos: { [key: string]: string } = {
  pendiente: 'Recibido',
  en_validacion: 'En Validación',
  correccion: 'Para Corrección',
  aprobado: 'Emitido',
  rechazado: 'Rechazado'
}

export default function SolicitudDetalle() {
  const params = useParams()
  const id = params?.id
  const [solicitud, setSolicitud] = useState<Solicitud | null>(null)

  const cargarSolicitud = () => {
    const token = localStorage.getItem('token')
    if (!token) return alert('Usuario no autenticado')

    fetch(`http://localhost:8000/requests/${id}`, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })
      .then(res => res.json())
      .then(data => setSolicitud(data))
      .catch(() => alert('Error al cargar la solicitud'))
  }

  useEffect(() => {
    if (id) cargarSolicitud()
  }, [id])

  const cerrarSesion = () => {
    localStorage.clear()
    window.location.href = '/login'
  }

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold text-blue-700">📄 Detalle de la Solicitud #{id}</h1>
        <button
          onClick={cerrarSesion}
          className="bg-red-600 text-white px-4 py-2 rounded hover:bg-red-700"
        >
          Cerrar sesión
        </button>
      </div>

      {solicitud ? (
        <div className="bg-white rounded shadow-md p-6 space-y-4">
          <p><span className="font-semibold">Solicitante:</span> {solicitud.nombre_usuario} {solicitud.apellido_usuario}</p>
          <p><span className="font-semibold">Tipo:</span> {solicitud.tipo === 'estudios' ? 'Estudios' : 'Nacimiento'}</p>
          <p><span className="font-semibold">Estado:</span> {estadosTraducidos[solicitud.estado] || solicitud.estado}</p>

          {solicitud.documento_url && (
            <div className="mt-4">
              <p className="font-semibold">📎 Documento enviado:</p>
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
      ) : (
        <p className="text-center text-gray-600">Cargando datos de la solicitud...</p>
      )}
    </div>
  )
}
