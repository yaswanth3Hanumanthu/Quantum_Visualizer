# Quick Test Reference Card

## 🚀 Start Testing Immediately

### Test 1: Basic Hadamard (1 minute)
1. Go to Circuit Builder
2. Set qubits: 1
3. Add gate: H(0)
4. Run Simulation
5. **Check**: Bloch sphere shows point on equator, purity = 1.0

### Test 2: Bell State (2 minutes)
1. Go to Circuit Builder
2. Set qubits: 2
3. Add gates: H(0), CX(0,1)
4. Run Simulation
5. **Check**: Both qubits show red (mixed), purity = 0.5 each

### Test 3: Quick Circuit Button
1. Go to Circuit Builder
2. Click "Load Bell State" button
3. Run Simulation
4. **Check**: Same results as Test 2

## 🔍 What to Look For

### ✅ Success Indicators
- No error messages in browser console
- Bloch spheres render properly
- Purity values are correct (1.0 for pure, <1.0 for mixed)
- Measurement counts make sense
- Circuit diagram displays

### ❌ Problem Signs
- "ImportError" messages
- Blank Bloch spheres
- Purity always 1.0 (partial trace not working)
- No measurement results
- Circuit diagram missing

## 🎯 Critical Tests

**Must Pass:**
1. **Hadamard Gate** - Basic quantum operation
2. **Bell State** - Entanglement detection
3. **Circuit Display** - Visual representation
4. **Simulation** - No runtime errors

**Nice to Have:**
- Step-by-step evolution
- Export functionality
- OpenQASM import
- Advanced gates (rotation, phase)

## 🚨 If Tests Fail

1. **Check Dependencies**: `pip list | grep qiskit`
2. **Restart App**: Stop and run `streamlit run app.py` again
3. **Browser Console**: Look for JavaScript errors
4. **Circuit Creation**: Verify gates were added correctly

## 📱 Quick Navigation

- **Home**: Project overview and status
- **Circuit Builder**: Create and test circuits
- **Simulation**: View results and measurements
- **Visualization**: Bloch spheres and analysis
- **Step-by-Step**: Circuit evolution
- **Export**: Download results

## 🎉 Success Criteria

Your QTrace installation is working if:
- ✅ App starts without errors
- ✅ Can create a 1-qubit circuit with H gate
- ✅ Simulation runs and shows results
- ✅ Bloch sphere displays correctly
- ✅ Purity calculation works
- ✅ Can navigate between pages

**Time to complete all tests: 10-15 minutes**
