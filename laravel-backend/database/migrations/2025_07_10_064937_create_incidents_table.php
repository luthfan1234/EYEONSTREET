<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    /**
     * Run the migrations.
     */
    public function up(): void
    {
        Schema::create('incidents', function (Blueprint $table) {
        $table->id(); // Kolom nomor urut (Primary Key)
        $table->string('cctv_id'); // Untuk nama CCTV, misal: "Banjarsari"
        $table->string('type'); // Untuk tipe insiden, misal: "accident" atau "crowd"
        $table->string('image_path'); // Untuk menyimpan path file gambar, misal: "screenshots/kejadian-123.jpg"
        $table->timestamps(); // Kolom created_at dan updated_at
    });

    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('incidents');
    }
};
