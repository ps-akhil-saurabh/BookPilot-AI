import React, { useState, useEffect } from 'react';
import { BookOpen, Plus } from 'lucide-react';
import { api } from '../services/api';
import type { Book } from '../types';

export const Library: React.FC = () => {
  const [books, setBooks] = useState<Book[]>([]);
  const [showAddModal, setShowAddModal] = useState(false);
  const [title, setTitle] = useState('');
  const [author, setAuthor] = useState('');
  const [pages, setPages] = useState(300);
  const [uploadFile, setUploadFile] = useState<File | null>(null);

  const loadBooks = () => {
    api.getBooks().then(setBooks).catch(console.error);
  };

  useEffect(() => {
    loadBooks();
  }, []);

  const handleAddBook = async (e: React.FormEvent) => {
    e.preventDefault();
    if (uploadFile) {
      const formData = new FormData();
      formData.append('file', uploadFile);
      if (title) formData.append('title', title);
      if (author) formData.append('author', author);
      await api.uploadBook(formData);
    } else {
      await api.addBook({ title, author, total_pages: Number(pages) });
    }
    setShowAddModal(false);
    setTitle('');
    setAuthor('');
    setUploadFile(null);
    loadBooks();
  };

  return (
    <div className="space-y-6 pb-12">
      {/* Top Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-slate-900 dark:text-white">Reading Library</h1>
          <p className="text-xs text-slate-500">Manage your books, PDFs, and uploaded resources.</p>
        </div>
        <button
          onClick={() => setShowAddModal(true)}
          className="inline-flex items-center gap-2 px-4 py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-700 text-white font-semibold text-sm shadow-md transition"
        >
          <Plus className="w-4 h-4" /> Add or Upload Book
        </button>
      </div>

      {/* Book Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
        {books.map((book) => (
          <div key={book.id} className="glass-card rounded-2xl border p-5 flex flex-col justify-between hover:shadow-lg transition">
            <div className="space-y-3">
              <div className="w-full h-40 rounded-xl bg-gradient-to-tr from-slate-200 to-indigo-100 dark:from-slate-800 dark:to-slate-700 flex items-center justify-center relative overflow-hidden">
                <BookOpen className="w-12 h-12 text-indigo-500 opacity-60" />
                {book.is_uploaded && (
                  <span className="absolute top-2 right-2 px-2 py-0.5 rounded-full bg-cyan-500 text-white text-[10px] font-bold">
                    RAG Indexed
                  </span>
                )}
              </div>
              <div>
                <span className="text-[10px] font-semibold text-indigo-500 uppercase tracking-wider">{book.genre || 'General'}</span>
                <h3 className="font-bold text-base text-slate-900 dark:text-white line-clamp-1">{book.title}</h3>
                <p className="text-xs text-slate-500 dark:text-slate-400">{book.author || 'Unknown Author'}</p>
              </div>
            </div>

            <div className="pt-4 border-t border-slate-200 dark:border-slate-700/60 mt-4 space-y-2">
              <div className="flex justify-between text-xs text-slate-500">
                <span>{book.total_pages} Pages</span>
                <span className="capitalize text-amber-500 font-medium">{book.difficulty}</span>
              </div>
              {/* Progress Bar */}
              <div className="w-full h-2 rounded-full bg-slate-200 dark:bg-slate-700 overflow-hidden">
                <div
                  className="h-full bg-indigo-600 rounded-full"
                  style={{ width: `${book.progress || 0}%` }}
                ></div>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Add / Upload Modal */}
      {showAddModal && (
        <div className="fixed inset-0 z-50 bg-black/50 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="glass-panel p-6 rounded-2xl border max-w-md w-full space-y-4">
            <h2 className="text-lg font-bold text-slate-900 dark:text-white">Add or Upload Book</h2>
            <form onSubmit={handleAddBook} className="space-y-4 text-sm">
              <div>
                <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">Book Title</label>
                <input
                  type="text"
                  required
                  value={title}
                  onChange={(e) => setTitle(e.target.value)}
                  placeholder="e.g. Atomic Habits"
                  className="w-full px-3 py-2 rounded-xl bg-slate-100 dark:bg-slate-800 border focus:outline-none"
                />
              </div>
              <div>
                <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">Author</label>
                <input
                  type="text"
                  value={author}
                  onChange={(e) => setAuthor(e.target.value)}
                  placeholder="e.g. James Clear"
                  className="w-full px-3 py-2 rounded-xl bg-slate-100 dark:bg-slate-800 border focus:outline-none"
                />
              </div>
              <div>
                <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">Total Pages</label>
                <input
                  type="number"
                  value={pages}
                  onChange={(e) => setPages(Number(e.target.value))}
                  className="w-full px-3 py-2 rounded-xl bg-slate-100 dark:bg-slate-800 border focus:outline-none"
                />
              </div>
              <div>
                <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">Upload File (PDF/EPUB/MD for RAG)</label>
                <input
                  type="file"
                  accept=".pdf,.epub,.md"
                  onChange={(e) => setUploadFile(e.target.files?.[0] || null)}
                  className="w-full text-xs text-slate-500 file:mr-3 file:py-2 file:px-4 file:rounded-xl file:border-0 file:text-xs file:font-semibold file:bg-indigo-50 file:text-indigo-700 hover:file:bg-indigo-100"
                />
              </div>
              <div className="flex justify-end gap-3 pt-2">
                <button
                  type="button"
                  onClick={() => setShowAddModal(false)}
                  className="px-4 py-2 rounded-xl text-slate-500 hover:bg-slate-100 dark:hover:bg-slate-800 text-xs font-semibold"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 rounded-xl bg-indigo-600 text-white text-xs font-semibold hover:bg-indigo-700"
                >
                  Save Book
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};
