<?php

namespace App\Jobs;

use App\Models\Incident;
use Illuminate\Bus\Queueable;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Bus\Dispatchable;
use Illuminate\Queue\InteractsWithQueue;
use Illuminate\Queue\SerializesModels;
use Illuminate\Support\Facades\Http;
use Illuminate\Support\Facades\Log;

class SendWablasNotification implements ShouldQueue
{
    use Dispatchable, InteractsWithQueue, Queueable, SerializesModels;

    protected $incident;

    /**
     * Create a new job instance.
     */
    public function __construct(Incident $incident)
    {
        $this->incident = $incident;
    }

    /**
     * Execute the job.
     */
    public function handle(): void
    {
        $server = config('services.wablas.server');
        $apiKey = config('services.wablas.api_key');
        $recipient = config('services.wablas.recipient_phone_number');

        if (!$server || !$apiKey || !$recipient) {
            Log::error('Kredensial Wablas tidak dikonfigurasi dengan benar.');
            return;
        }

        // Siapkan pesan yang akan dikirim
        $message = "🚨 *PERINGATAN INSIDEN* 🚨\n\n";
        $message .= "Telah terdeteksi adanya potensi *Kecelakaan*.\n\n";
        $message .= "Lokasi: *CCTV " . $this->incident->cctv_id . "*\n";
        $message .= "Waktu: *" . now()->format('d-m-Y H:i:s') . "*\n\n";
        $message .= "Harap segera periksa dan tindak lanjuti.";

        // Kirim request ke API Wablas menggunakan Laravel HTTP Client
        $response = Http::withHeaders([
            'Authorization' => $apiKey
        ])->post("{$server}/api/send-message", [
            'phone' => $recipient,
            'message' => $message,
        ]);

        if ($response->successful()) {
            Log::info('Notifikasi WhatsApp berhasil dikirim untuk insiden ID: ' . $this->incident->id);
        } else {
            Log::error('Gagal mengirim notifikasi WhatsApp: ' . $response->body());
        }
    }
}
