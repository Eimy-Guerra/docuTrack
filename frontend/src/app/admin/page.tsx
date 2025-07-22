'use client'

import { useEffect, useState } from "react"

type Solicitud = {
  id: number
  tipo: string
  estado: string
  nombre_usuario: string
  apellido_usuario: string
}

const estadosTraducidos: { [key: string]: string } = {
  pendiente: "Recibido",
  en_validacion: "En Validación",
  correccion: "Para Corrección",
  aprobado: "Emitido",
  rechazado: "Rechazado"
}

export default function AdminDashboard() {
  const [solicitudes, setSolicitudes] = useState<Solicitud[]>([])
  const [loading, setLoading] = useState(true)

  const cargarSolicitudes = () => {
    const token = localStorage.getItem("token")
    if (!token) return alert("Usuario no autenticado")

    fetch("http://localhost:8000/requests/", {
      headers: { Authorization: `Bearer ${token}` }
    })
      .then(res => res.json())
      .then(data => {
        setSolicitudes(data)
        setLoading(false)
      })
      .catch(() => {
        alert("Error al cargar solicitudes")
        setLoading(false)
      })
  }

  useEffect(() => {
    cargarSolicitudes()
  }, [])

  const validarSolicitud = async (id: number, estado: string) => {
    const token = localStorage.getItem("token")
    if (!token) return alert("No estás autenticado")

    if (estado === "pendiente") {
      try {
        const res = await fetch(`http://localhost:8000/requests/${id}/validar`, {
          method: "PUT",
          headers: { Authorization: `Bearer ${token}` }
        })

        const data = await res.json()
        if (res.ok) {
          alert(`✅ Solicitud #${id} marcada como 'En Validación'`)
          window.location.href = `/admin/solicitud/${id}`
        } else {
          alert(data.detail || "Error al validar solicitud")
        }
      } catch {
        alert("Error de conexión al validar")
      }
    } else {
      window.location.href = `/admin/solicitud/${id}` // Solo redirige
    }
  }

  const cerrarSesion = () => {
    localStorage.clear()
    window.location.href = "/login"
  }

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold text-blue-700">📊 Dashboard de Administradores</h1>
        <button
          onClick={cerrarSesion}
          className="bg-red-600 text-white px-4 py-2 rounded hover:bg-red-700"
        >
          Cerrar sesión
        </button>
      </div>

      {loading && <p className="text-center">Cargando solicitudes...</p>}

      {!loading && solicitudes.length === 0 && (
        <p className="text-center text-gray-600">No hay solicitudes en el sistema.</p>
      )}

      <div className="overflow-x-auto">
        <table className="w-full bg-white rounded shadow-md">
          <thead className="bg-blue-100 text-blue-700">
            <tr>
              <th className="py-3 px-4 text-left">Solicitante</th>
              <th className="py-3 px-4 text-left">Tipo</th>
              <th className="py-3 px-4 text-left">Estado</th>
              <th className="py-3 px-4 text-left">Acción</th>
            </tr>
          </thead>
          <tbody>
            {solicitudes.map((solicitud) => (
              <tr key={solicitud.id} className="border-t">
                <td className="py-2 px-4">{solicitud.nombre_usuario} {solicitud.apellido_usuario}</td>
                <td className="py-2 px-4">
                  {String(solicitud.tipo || "").toLowerCase().includes("estudio") ? "Estudios" : "Nacimiento"}
                </td>
                <td className="py-2 px-4">
                  <span className="font-medium text-green-700">
                    {estadosTraducidos[solicitud.estado] || solicitud.estado}
                  </span>
                </td>
                <td className="py-2 px-4">
                  {["pendiente", "en_validacion"].includes(solicitud.estado) && (
                    <button
                      onClick={() => validarSolicitud(solicitud.id, solicitud.estado)}
                      className="bg-yellow-500 text-white px-3 py-1 rounded hover:bg-yellow-600"
                    >
                      Validar
                    </button>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
