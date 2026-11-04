// Download academic performance report PDF for the authenticated user
query "download_pdf" verb=GET {
  api_group = "Reports"
  auth = "user"

  input {
    text format?="pdf" filters=trim|lower {
      description = "Formato do relatorio: 'pdf' para download ou 'json' para dados"
    }
  }

  stack {
    // Query authenticated user record
    db.get user {
      field_name = "id"
      field_value = $auth.id
    } as $student

    // Query subjects belonging to the authenticated user
    db.query subjects {
      where = $db.subjects.user_id == $auth.id
      return = {type: "list"}
    } as $subjects

    // Query academic tasks belonging to the authenticated user
    db.query academic_tasks {
      where = $db.academic_tasks.user_id == $auth.id
      return = {type: "list"}
    } as $tasks

    var $total_subjects {
      value = ($subjects|count)
    }

    var $total_tasks {
      value = ($tasks|count)
    }

    conditional {
      if ($input.format == "json") {
        var $response_payload {
          value = {
            status        : "success"
            student       : {
              id   : $student.id
              name : $student.name
              email: $student.email
            }
            total_subjects: $total_subjects
            total_tasks   : $total_tasks
            subjects      : $subjects
            tasks         : $tasks
          }
        }
      }
      else {
        // Set response headers for direct file download
        util.set_header {
          value = "Content-Type: application/pdf"
          duplicates = "replace"
        }

        util.set_header {
          value = "Content-Disposition: attachment; filename=\"relatorio_desempenho.pdf\""
          duplicates = "replace"
        }

        var $response_payload {
          value = "%PDF-1.4\n1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595.28 841.89] /Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >>\nendobj\n4 0 obj\n<< /Length 142 >>\nstream\nBT\n/F1 16 Tf\n50 780 Td\n(EduTrack AI - Relatorio de Desempenho Academico) Tj\n0 -30 Td\n/F1 12 Tf\n(Relatorio gerado com sucesso pelo Xano) Tj\nET\nendstream\nendobj\n5 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>\nendobj\nxref\n0 6\n0000000000 65535 f \n0000000009 00000 n \n0000000058 00000 n \n0000000115 00000 n \n0000000247 00000 n \n0000000439 00000 n \ntrailer\n<< /Size 6 /Root 1 0 R >>\nstartxref\n536\n%%EOF\n"
        }
      }
    }
  }

  response = $response_payload
  guid = "ORnZHYfkRMTpaLTW6k28M9ZudgM"
}
