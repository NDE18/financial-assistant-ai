import React, { useState, useRef } from 'react';
import { invoiceService } from '../../services/invoiceService';
import { Upload, FileText, CheckCircle, XCircle, Loader } from 'lucide-react';

interface InvoiceUploadProps {
  onUploadComplete: () => void;
}

const InvoiceUpload: React.FC<InvoiceUploadProps> = ({ onUploadComplete }) => {
  const [file, setFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [dragActive, setDragActive] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFile(e.dataTransfer.files[0]);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    e.preventDefault();
    if (e.target.files && e.target.files[0]) {
      handleFile(e.target.files[0]);
    }
  };

  const handleFile = (selectedFile: File) => {
    const validTypes = ['image/jpeg', 'image/png', 'image/jpg', 'application/pdf'];
    if (!validTypes.includes(selectedFile.type)) {
      alert('Type de fichier non supporté. Utilisez JPG, PNG ou PDF.');
      return;
    }

    if (selectedFile.size > 10 * 1024 * 1024) {
      alert('Le fichier est trop volumineux (max 10MB).');
      return;
    }

    setFile(selectedFile);
  };

  const handleUpload = async () => {
    if (!file) return;

    setUploading(true);
    try {
      await invoiceService.upload(file);
      setFile(null);
      onUploadComplete();
      alert('Facture téléchargée avec succès! L\'extraction OCR est en cours...');
    } catch (error) {
      console.error('Error uploading invoice:', error);
      alert('Erreur lors du téléchargement de la facture.');
    } finally {
      setUploading(false);
    }
  };

  const onButtonClick = () => {
    fileInputRef.current?.click();
  };

  return (
    <div className="bg-white rounded-xl shadow-md p-6">
      <h3 className="text-lg font-bold text-gray-900 mb-4">Télécharger une Facture</h3>

      <div
        className={`border-2 border-dashed rounded-lg p-8 text-center transition ${
          dragActive
            ? 'border-blue-500 bg-blue-50'
            : 'border-gray-300 hover:border-gray-400'
        }`}
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
      >
        <input
          ref={fileInputRef}
          type="file"
          accept=".jpg,.jpeg,.png,.pdf"
          onChange={handleChange}
          className="hidden"
        />

        {!file ? (
          <div>
            <Upload className="w-12 h-12 text-gray-400 mx-auto mb-4" />
            <p className="text-gray-600 mb-2">
              Glissez-déposez votre facture ici ou
            </p>
            <button
              onClick={onButtonClick}
              className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition"
            >
              Parcourir les fichiers
            </button>
            <p className="text-xs text-gray-500 mt-2">
              Formats supportés: JPG, PNG, PDF (max 10MB)
            </p>
          </div>
        ) : (
          <div>
            <FileText className="w-12 h-12 text-blue-600 mx-auto mb-4" />
            <p className="font-medium text-gray-900">{file.name}</p>
            <p className="text-sm text-gray-500 mb-4">
              {(file.size / 1024 / 1024).toFixed(2)} MB
            </p>
            <div className="flex justify-center space-x-3">
              <button
                onClick={() => setFile(null)}
                className="px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50"
                disabled={uploading}
              >
                Changer
              </button>
              <button
                onClick={handleUpload}
                disabled={uploading}
                className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 flex items-center space-x-2"
              >
                {uploading ? (
                  <>
                    <Loader className="w-4 h-4 animate-spin" />
                    <span>Téléchargement...</span>
                  </>
                ) : (
                  <span>Télécharger</span>
                )}
              </button>
            </div>
          </div>
        )}
      </div>

      <div className="mt-4 bg-blue-50 rounded-lg p-4">
        <p className="text-sm text-blue-800">
          <strong>ℹ️ Extraction automatique:</strong> Une fois téléchargée, l'IA extraira
          automatiquement les informations (montant, date, fournisseur) et créera une transaction.
        </p>
      </div>
    </div>
  );
};

export default InvoiceUpload;