import * as XLSX from 'xlsx';

export function useExport(data) {
  // Converte o objeto { domain: [emails] } para um array plano
  const getFlatData = () => {
    return Object.entries(data.value).flatMap(([domain, emails]) => 
      emails.map(email => ({ Domain: domain, Email: email }))
    );
  };

  // Exportar para JSON
  const exportToJson = () => {
    const jsonString = JSON.stringify(data.value, null, 2);
    const blob = new Blob([jsonString], { type: 'application/json' });
    downloadBlob(blob, 'contatos.json');
  };

  // Exportar para CSV
  const exportToCsv = () => {
    const flatData = getFlatData();
    let csvContent = "Domain,Email\n";
    flatData.forEach(item => {
      csvContent += `${item.Domain},${item.Email}\n`;
    });
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    downloadBlob(blob, 'contatos.csv');
  };

  // Exportar para Excel
  const exportToExcel = () => {
    const flatData = getFlatData();
    const worksheet = XLSX.utils.json_to_sheet(flatData);
    const workbook = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(workbook, worksheet, 'Contatos');
    XLSX.writeFile(workbook, 'contatos.xlsx');
  };
  
  // Função auxiliar para download
  const downloadBlob = (blob, filename) => {
    const link = document.createElement('a');
    const url = URL.createObjectURL(blob);
    link.setAttribute('href', url);
    link.setAttribute('download', filename);
    link.style.visibility = 'hidden';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  // Retornamos apenas as funções de exportação disponíveis
  return { exportToJson, exportToCsv, exportToExcel };
}