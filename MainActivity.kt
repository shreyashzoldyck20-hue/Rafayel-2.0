package com.rafayel.assistant

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.itemsIndexed
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.RequestBody.Companion.toRequestBody
import org.json.JSONObject
import java.util.concurrent.TimeUnit

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent { RafayelScreen() }
    }
}

data class ChatLine(val role: String, val text: String)

@Composable
fun RafayelScreen() {
    val lines = remember { mutableStateListOf(ChatLine("RAFAYEL", "I’m RAFAYEL. Connect to your shared AI brain and let’s begin.")) }
    var input by remember { mutableStateOf("") }
    var conversation by remember { mutableStateOf<String?>(null) }
    var busy by remember { mutableStateOf(false) }
    var error by remember { mutableStateOf("") }
    val scope = rememberCoroutineScope()
    val client = remember { OkHttpClient.Builder().callTimeout(90, TimeUnit.SECONDS).build() }

    MaterialTheme(colorScheme = darkColorScheme(primary = Color(0xFFD8AC70), background = Color(0xFF050914))) {
        Column(Modifier.fillMaxSize().background(Brush.verticalGradient(listOf(Color(0xFF10213A), Color(0xFF050914)))).padding(18.dp)) {
            Text("✦  R A F A Y E L", color = Color(0xFFE8C18C), fontSize = 21.sp)
            Text("THE COSMIC INTELLIGENCE", color = Color(0xFF8197B2), fontSize = 9.sp)
            Spacer(Modifier.height(18.dp))
            Box(Modifier.fillMaxWidth().height(130.dp), contentAlignment = Alignment.Center) {
                Text("◉", color = Color(0xFFD7A66C), fontSize = 86.sp)
            }
            LazyColumn(Modifier.weight(1f).fillMaxWidth()) {
                itemsIndexed(lines) { _, line ->
                    Column(Modifier.fillMaxWidth().padding(vertical = 6.dp).background(if (line.role == "YOU") Color(0xFF172A3D) else Color(0xFF101D2D), RoundedCornerShape(12.dp)).padding(12.dp)) {
                        Text(line.role, color = Color(0xFFD8AC70), fontSize = 9.sp)
                        Text(line.text, color = Color(0xFFE8EDF8), fontSize = 14.sp)
                    }
                }
            }
            if (error.isNotBlank()) Text(error, color = Color(0xFFFF9C91), fontSize = 11.sp)
            Row(verticalAlignment = Alignment.CenterVertically) {
                OutlinedTextField(value = input, onValueChange = { input = it }, modifier = Modifier.weight(1f), placeholder = { Text("Talk to RAFAYEL…") }, maxLines = 3)
                Spacer(Modifier.width(8.dp))
                Button(enabled = !busy && input.isNotBlank(), onClick = {
                    val msg = input.trim()
                    input = ""
                    lines.add(ChatLine("YOU", msg))
                    busy = true
                    error = ""
                    scope.launch {
                        try {
                            val result = withContext(Dispatchers.IO) {
                                val payload = JSONObject().put("message", msg).also { conversation?.let { id -> it.put("conversation_id", id) } }
                                val body = payload.toString().toRequestBody("application/json".toMediaType())
                                val req = Request.Builder().url(BuildConfig.API_BASE_URL + "api/chat").post(body).build()
                                client.newCall(req).execute().use { response ->
                                    val text = response.body?.string().orEmpty()
                                    if (!response.isSuccessful) throw Exception(JSONObject(text).optString("detail", "API error ${response.code}"))
                                    JSONObject(text)
                                }
                            }
                            conversation = result.optString("conversation_id")
                            lines.add(ChatLine("RAFAYEL", result.optString("reply", "No reply returned.")))
                        } catch (e: Exception) {
                            error = "Can't reach RAFAYEL backend: ${e.message}"
                        } finally { busy = false }
                    }
                }) { Text(if (busy) "…" else "SEND") }
            }
            Text("HYBRID AI • SHARED MEMORY • YOU STAY IN CONTROL", color = Color(0xFF8197B2), fontSize = 8.sp, modifier = Modifier.padding(top = 12.dp))
        }
    }
}
