<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Models\Incident;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Storage;
use Illuminate\Support\Str;
use App\Jobs\SendWablasNotification; // 1. Import Job untuk Wablas

class IncidentController extends Controller
{
    public function index()
    {
        // Ambil semua data insiden, urutkan dari yang terbaru
        $incidents = Incident::latest()->get();
        return response()->json($incidents);
    }

    /**
     * Menyimpan data insiden baru dari AI.
     */
    public function store(Request $request)
    {
        // 1. Validasi data yang masuk dari Python
        $validated = $request->validate([
            'cctv_id' => 'required|string|max:255',
            'type' => 'required|string|in:accident,crowd',
            'image_base64' => 'required|string',
        ]);

        // 2. Decode gambar dari Base64 dan siapkan path penyimpanan
        $image_parts = explode(";base64,", $validated['image_base64']);
        $image_type_aux = explode("image/", $image_parts[0]);
        $image_type = $image_type_aux[1] ?? 'jpg';
        $image_base64 = base64_decode($image_parts[1]);

        // Buat nama file yang unik
        $filename = 'incident-' . Str::uuid() . '.' . $image_type;
        $filepath = 'screenshots/' . $filename;

        // 3. Simpan file gambar ke dalam storage
        Storage::disk('public')->put($filepath, $image_base64);

        // 4. Simpan data kejadian ke database melalui Model
        $incident = Incident::create([
            'cctv_id' => $validated['cctv_id'],
            'type' => $validated['type'],
            'image_path' => $filepath, // Simpan path-nya ke database
        ]);

        // 5. (PERUBAHAN) Jika tipe insiden adalah 'accident', panggil job untuk WhatsApp
        if ($incident->type === 'accident') {
            SendWablasNotification::dispatch($incident);
        }

        // 6. Beri respon sukses dalam format JSON
        return response()->json([
            'message' => 'Incident reported successfully.',
            'data' => $incident,
        ], 201); // 201 artinya 'Created'
    }
}
