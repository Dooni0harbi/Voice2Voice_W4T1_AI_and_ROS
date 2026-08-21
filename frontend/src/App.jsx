import {
  Mic,
  Square,
  RotateCcw,
  LoaderCircle,
  Volume2,
} from "lucide-react";

import { useRef, useState } from "react";

const API_URL = "http://127.0.0.1:8000";

export default function App() {
  const [isRecording, setIsRecording] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);

  const [status, setStatus] = useState("جاهز للتسجيل");
  const [error, setError] = useState("");

  const [transcript, setTranscript] = useState("");
  const [reply, setReply] = useState("");

  const mediaRecorderRef = useRef(null);
  const streamRef = useRef(null);
  const chunksRef = useRef([]);
  const audioReplyRef = useRef(null);

  // =====================================================
  // START RECORDING
  // =====================================================

  const startRecording = async () => {
    try {
      setError("");
      setTranscript("");
      setReply("");

      const stream = await navigator.mediaDevices.getUserMedia({
        audio: true,
      });

      streamRef.current = stream;

      let options = {};

      if (MediaRecorder.isTypeSupported("audio/webm;codecs=opus")) {
        options = {
          mimeType: "audio/webm;codecs=opus",
        };
      }

      const recorder = new MediaRecorder(stream, options);

      mediaRecorderRef.current = recorder;
      chunksRef.current = [];

      recorder.ondataavailable = (event) => {
        if (event.data && event.data.size > 0) {
          chunksRef.current.push(event.data);
        }
      };

      recorder.onstop = handleRecordingFinished;

      recorder.start();

      setIsRecording(true);
      setStatus("أسمعك الآن...");
    } catch (err) {
      console.error(err);

      setError("لم أتمكن من الوصول إلى الميكروفون.");
    }
  };

  // =====================================================
  // STOP RECORDING
  // =====================================================

  const stopRecording = () => {
    if (
      !mediaRecorderRef.current ||
      mediaRecorderRef.current.state === "inactive"
    ) {
      return;
    }

    mediaRecorderRef.current.stop();

    setIsRecording(false);
    setStatus("جاري إرسال التسجيل...");

    if (streamRef.current) {
      streamRef.current.getTracks().forEach((track) => {
        track.stop();
      });
    }
  };

  // =====================================================
  // TOGGLE RECORDING
  // =====================================================

  const toggleRecording = () => {
    if (isProcessing) {
      return;
    }

    if (isRecording) {
      stopRecording();
    } else {
      startRecording();
    }
  };

  // =====================================================
  // RECORDING FINISHED
  // =====================================================

  const handleRecordingFinished = async () => {
    const blob = new Blob(chunksRef.current, {
      type:
        mediaRecorderRef.current?.mimeType ||
        "audio/webm",
    });

    const file = new File(
      [blob],
      "recording.webm",
      {
        type: blob.type || "audio/webm",
      }
    );

    await sendVoice(file);
  };

  // =====================================================
  // SEND AUDIO TO BACKEND
  // =====================================================

  const sendVoice = async (file) => {
    try {
      setIsProcessing(true);
      setError("");
      setStatus("جاري التفكير...");

      const formData = new FormData();

      formData.append("audio", file);

      const response = await fetch(
        `${API_URL}/api/voice`,
        {
          method: "POST",
          body: formData,
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail ||
            "حدث خطأ أثناء معالجة الصوت."
        );
      }

      setTranscript(data.transcript || "");
      setReply(data.reply || "");

      setStatus("تم إنشاء الرد");

      if (data.audio && audioReplyRef.current) {
        audioReplyRef.current.src = data.audio;

        try {
          await audioReplyRef.current.play();

          setStatus("يتم تشغيل الرد...");
        } catch (playError) {
          console.warn(
            "Autoplay blocked:",
            playError
          );

          setStatus("الرد الصوتي جاهز");
        }
      }
    } catch (err) {
      console.error(err);

      setError(err.message);

      setStatus(
        "جاهز للمحاولة مرة أخرى"
      );
    } finally {
      setIsProcessing(false);
    }
  };

  // =====================================================
  // RESET
  // =====================================================

  const resetConversation = async () => {
    try {
      await fetch(`${API_URL}/api/reset`, {
        method: "POST",
      });
    } catch (err) {
      console.error(err);
    }

    setTranscript("");
    setReply("");
    setError("");
    setStatus("جاهز للتسجيل");
  };

  // =====================================================
  // UI
  // =====================================================

  return (
    <main
      dir="rtl"
      className="
        relative
        min-h-screen
        overflow-hidden
        px-5
        py-12
        text-white
        flex
        items-center
        justify-center
        bg-[radial-gradient(circle_at_15%_15%,rgba(147,16,67,0.75),transparent_34%),radial-gradient(circle_at_85%_85%,rgba(24,109,124,0.78),transparent_34%),linear-gradient(135deg,#151827_0%,#090b12_50%,#07181a_100%)]
      "
    >
      {/* BACKGROUND GLOWS */}

      <div
        className="
          pointer-events-none
          absolute
          -top-24
          right-[18%]
          h-72
          w-72
          rounded-full
          bg-[#931043]/45
          blur-[110px]
        "
      />

      <div
        className="
          pointer-events-none
          absolute
          -bottom-20
          left-[15%]
          h-64
          w-64
          rounded-full
          bg-[#186D7C]/50
          blur-[110px]
        "
      />

      {/* GLASS CARD */}

      <section
        className="
          smart-glass
          relative
          z-10
          w-full
          max-w-[520px]
          overflow-hidden
          rounded-[34px]
          px-8
          py-10
          sm:px-12
          sm:py-12
        "
      >
        {/* GLASS HIGHLIGHT */}

        <div
          className="
            pointer-events-none
            absolute
            -left-20
            -top-24
            h-52
            w-72
            rotate-[-18deg]
            bg-white/10
            blur-3xl
          "
        />

        {/* BRAND */}

        <div
          className="
            relative
            z-10
            mb-7
            flex
            items-center
            justify-center
            gap-2
            text-xs
            font-extrabold
            tracking-[0.22em]
            text-[#65c7d1]
          "
        >
          <span
            className="
              h-2
              w-2
              rounded-full
              bg-[#c32c68]
              shadow-[0_0_16px_rgba(195,44,104,0.8)]
            "
          />

          SMART METHODS
        </div>

        {/* HERO */}

        <div
          className="
            relative
            z-10
            text-center
          "
        >
          <h1
            className="
              m-0
              text-4xl
              font-medium
              leading-tight
              sm:text-[44px]
            "
          >
            مساعدك
          </h1>

          <h2
            className="
              -mt-1
              text-6xl
              font-black
              leading-tight
              text-[#d53b76]
              drop-shadow-[0_12px_30px_rgba(147,16,67,0.3)]
              sm:text-[66px]
            "
          >
            الصوتي
          </h2>

          <p
            className="
              mx-auto
              mt-5
              max-w-[390px]
              text-sm
              font-medium
              leading-8
              text-white/65
            "
          >
            تحدث مع المساعد الذكي، وسيجيب عن جميع استفساراتك المتعلقة بشركة سمارت ميثودز.
            اضغط على المايك وابدأ الحديث،
            ثم اضغط مرة أخرى لإرسال طلبك.
          </p>
        </div>

        {/* MIC SECTION */}

        <div
          className="
            relative
            z-10
            mt-9
            flex
            flex-col
            items-center
          "
        >
          <p
            className="
              mb-5
              text-sm
              font-bold
              text-white/80
            "
          >
            ابدأ المحادثة
          </p>

          <div
            className="
              relative
              flex
              items-center
              justify-center
            "
          >
            {isRecording && (
              <span
                className="
                  recording-ring
                  absolute
                  h-24
                  w-24
                  rounded-full
                  bg-[#F5514B]/40
                "
              />
            )}

            <button
              onClick={toggleRecording}
              disabled={isProcessing}
              className={`
                mic-glow
                relative
                z-10
                flex
                h-24
                w-24
                items-center
                justify-center
                rounded-full
                border
                border-white/25
                transition-all
                duration-300

                ${
                  isRecording
                    ? "bg-gradient-to-br from-[#F5514B] to-[#b51d47]"
                    : "bg-gradient-to-br from-[#a3124b] to-[#731035]"
                }

                ${
                  isProcessing
                    ? "cursor-wait opacity-70"
                    : "cursor-pointer hover:scale-105 active:scale-95"
                }
              `}
            >
              {isProcessing ? (
                <LoaderCircle
                  size={36}
                  strokeWidth={2.2}
                  className="
                    animate-spin
                    text-white
                  "
                />
              ) : isRecording ? (
                <Square
                  size={30}
                  strokeWidth={2.4}
                  fill="white"
                  className="text-white"
                />
              ) : (
                <Mic
                  size={38}
                  strokeWidth={2.3}
                  className="text-white"
                />
              )}
            </button>
          </div>

          {/* STATUS */}

          <div
            className="
              mt-5
              flex
              min-h-7
              items-center
              gap-2
              text-sm
              font-bold
              text-[#69cbd4]
            "
          >
            {isProcessing && (
              <LoaderCircle
                size={16}
                className="animate-spin"
              />
            )}

            {!isProcessing && reply && (
              <Volume2 size={16} />
            )}

            {status}
          </div>

          {/* ERROR */}

          {error && (
            <p
              className="
                mt-2
                max-w-sm
                text-center
                text-xs
                leading-5
                text-[#ff8799]
              "
            >
              {error}
            </p>
          )}

          {/* RESULT */}

          {(transcript || reply) && (
            <div
              className="
                mt-7
                w-full
                rounded-2xl
                border
                border-white/10
                bg-black/15
                p-4
                backdrop-blur-xl
              "
            >
              {transcript && (
                <div className="mb-3">
                  <span
                    className="
                      text-xs
                      font-bold
                      text-[#65c7d1]
                    "
                  >
                    أنتِ
                  </span>

                  <p
                    className="
                      mt-1
                      text-sm
                      leading-6
                      text-white/75
                    "
                  >
                    {transcript}
                  </p>
                </div>
              )}

              {reply && (
                <div>
                  <span
                    className="
                      text-xs
                      font-bold
                      text-[#d95b8c]
                    "
                  >
                    المساعد
                  </span>

                  <p
                    className="
                      mt-1
                      text-sm
                      leading-6
                      text-white/80
                    "
                  >
                    {reply}
                  </p>
                </div>
              )}
            </div>
          )}

          {/* RESET */}

          <button
            onClick={resetConversation}
            className="
              mt-8
              flex
              items-center
              gap-2
              rounded-xl
              border
              border-white/15
              bg-white/[0.06]
              px-5
              py-2.5
              text-xs
              font-bold
              text-white/65
              backdrop-blur-xl
              transition-all
              hover:border-[#186D7C]/60
              hover:bg-[#186D7C]/40
              hover:text-white
            "
          >
            <RotateCcw size={14} />

            مسح المحادثة
          </button>
        </div>

        <audio
          ref={audioReplyRef}
          className="hidden"
        />
      </section>
    </main>
  );
}