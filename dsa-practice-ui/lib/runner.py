import sys
import json
import time
import traceback
from typing import *
from collections import defaultdict, deque, Counter, OrderedDict
import heapq
import bisect
import math

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Node:
    def __init__(self, val=0, neighbors=None, next=None, random=None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []
        self.next = next
        self.random = random

def build_linked_list(vals):
    if not vals:
        return None
    dummy = ListNode(0)
    curr = dummy
    for v in vals:
        curr.next = ListNode(v)
        curr = curr.next
    return dummy.next

def build_binary_tree(vals):
    if not vals:
        return None
    root = TreeNode(vals[0])
    q = deque([root])
    i = 1
    while q and i < len(vals):
        node = q.popleft()
        if i < len(vals) and vals[i] is not None:
            node.left = TreeNode(vals[i])
            q.append(node.left)
        i += 1
        if i < len(vals) and vals[i] is not None:
            node.right = TreeNode(vals[i])
            q.append(node.right)
        i += 1
    return root

def serialize_res(val):
    if isinstance(val, (int, float, str, bool)) or val is None:
        return val
    if isinstance(val, (list, tuple)):
        return [serialize_res(x) for x in val]
    if isinstance(val, set):
        return sorted([serialize_res(x) for x in val])
    if isinstance(val, dict):
        return {str(k): serialize_res(v) for k, v in val.items()}
    if isinstance(val, ListNode):
        res = []
        curr = val
        while curr and len(res) < 1000:
            res.append(curr.val)
            curr = curr.next
        return res
    if isinstance(val, TreeNode):
        res = []
        q = deque([val])
        while q:
            node = q.popleft()
            if node:
                res.append(node.val)
                q.append(node.left)
                q.append(node.right)
            else:
                res.append(None)
        while res and res[-1] is None:
            res.pop()
        return res
    return str(val)

def run_payload(payload):
    user_code = payload.get('code', '')
    entry_fn = payload.get('entryFunction', '')
    testcases = payload.get('testcases', []) or payload.get('testCases', [])
    is_class = payload.get('isClass', False) or (bool(testcases) and 'methods' in testcases[0])

    import io
    stdout_buf = io.StringIO()
    old_stdout = sys.stdout
    sys.stdout = stdout_buf

    env = {
        'ListNode': ListNode,
        'TreeNode': TreeNode,
        'Node': Node,
        'build_linked_list': build_linked_list,
        'build_binary_tree': build_binary_tree,
        'math': math,
        'heapq': heapq,
        'bisect': bisect,
        'defaultdict': defaultdict,
        'deque': deque,
        'Counter': Counter,
        'OrderedDict': OrderedDict,
        'List': List,
        'Dict': Dict,
        'Set': Set,
        'Tuple': Tuple,
        'Optional': Optional,
    }

    try:
        # Step 1: Compile
        try:
            compiled = compile(user_code, '<solution>', 'exec')
        except SyntaxError as e:
            sys.stdout = old_stdout
            return {
                'status': 'Compile Error',
                'runtimeMs': 0,
                'passedCount': 0,
                'totalCount': len(testcases),
                'results': [],
                'error': f'SyntaxError: {e.msg} (line {e.lineno})',
                'stdout': stdout_buf.getvalue()
            }
        except Exception as e:
            sys.stdout = old_stdout
            return {
                'status': 'Compile Error',
                'runtimeMs': 0,
                'passedCount': 0,
                'totalCount': len(testcases),
                'results': [],
                'error': f'{type(e).__name__}: {str(e)}',
                'stdout': stdout_buf.getvalue()
            }

        # Step 2: Execute
        try:
            exec(compiled, env)
        except Exception as e:
            sys.stdout = old_stdout
            return {
                'status': 'Runtime Error',
                'runtimeMs': 0,
                'passedCount': 0,
                'totalCount': len(testcases),
                'results': [],
                'error': traceback.format_exc(),
                'stdout': stdout_buf.getvalue()
            }

        # Step 3: Identify caller candidates
        slug = payload.get('slug', '')
        sol_class = None
        target_fn = None
        fn_candidates = []

        if is_class and entry_fn in env and isinstance(env[entry_fn], type):
            target_class = env[entry_fn]
        else:
            if 'Solution' in env and isinstance(env['Solution'], type):
                sol_class = env['Solution']
                try:
                    sol = sol_class()
                    if hasattr(sol, entry_fn):
                        fn_candidates.append(getattr(sol, entry_fn))
                    else:
                        methods = [m for m in dir(sol) if not m.startswith('__')]
                        for m in methods:
                            fn_candidates.append(getattr(sol, m))
                except Exception:
                    pass

            if entry_fn in env and callable(env[entry_fn]) and not isinstance(env[entry_fn], type):
                if env[entry_fn] not in fn_candidates:
                    fn_candidates.append(env[entry_fn])

            builtin_names = {
                'ListNode', 'TreeNode', 'Node', 'build_linked_list', 'build_binary_tree',
                'math', 'heapq', 'bisect', 'defaultdict', 'deque', 'Counter', 'OrderedDict',
                'List', 'Dict', 'Set', 'Tuple', 'Optional', 'serialize_res', 'run_payload'
            }
            for k, v in env.items():
                if callable(v) and not isinstance(v, type) and k not in builtin_names and v not in fn_candidates:
                    fn_candidates.append(v)

            target_fn = fn_candidates[0] if fn_candidates else None

        def invoke_candidate(fn, args):
            try:
                return fn(*args)
            except TypeError as e1:
                if sol_class and hasattr(fn, '__name__') and hasattr(sol_class, fn.__name__):
                    try:
                        return getattr(sol_class, fn.__name__)(*args)
                    except Exception:
                        pass
                try:
                    return fn(None, *args)
                except Exception:
                    raise e1

        def check_is_passed(actual_ser, expected_ser, tc_item):
            if actual_ser == expected_ser:
                return True

            if isinstance(actual_ser, float) and isinstance(expected_ser, (int, float)):
                return abs(actual_ser - expected_ser) < 1e-4

            # Two Sum: allow indices in any order [0, 1] == [1, 0] or check nums[i] + nums[j] == target
            if slug == 'two-sum' or entry_fn == 'twoSum':
                if isinstance(actual_ser, (list, tuple)) and len(actual_ser) == 2:
                    if sorted(actual_ser) == sorted(expected_ser):
                        return True
                    args_list = tc_item.get('args', [])
                    if len(args_list) >= 2:
                        nums_arr, target_val = args_list[0], args_list[1]
                        i, j = actual_ser[0], actual_ser[1]
                        if isinstance(i, int) and isinstance(j, int) and i != j:
                            if 0 <= i < len(nums_arr) and 0 <= j < len(nums_arr):
                                if nums_arr[i] + nums_arr[j] == target_val:
                                    return True

            # Order-insensitive problems (sets, combinations, permutations)
            order_free_slugs = {
                'two-sum', 'two-sum-ii-input-array-is-sorted', '3sum', '4sum',
                'group-anagrams', 'top-k-frequent-elements', 'subsets', 'subsets-ii',
                'permutations', 'combination-sum', 'combination-sum-ii',
                'letter-combinations-of-a-phone-number', 'word-search-ii',
                'find-all-anagrams-in-a-string'
            }

            if tc_item.get('orderInsensitive') or slug in order_free_slugs:
                if isinstance(actual_ser, list) and isinstance(expected_ser, list):
                    if all(isinstance(x, list) for x in expected_ser):
                        try:
                            norm_act = sorted([sorted([str(i) for i in sub]) if isinstance(sub, list) else [str(sub)] for sub in actual_ser])
                            norm_exp = sorted([sorted([str(i) for i in sub]) if isinstance(sub, list) else [str(sub)] for sub in expected_ser])
                            if norm_act == norm_exp:
                                return True
                        except Exception:
                            pass
                    try:
                        if sorted([str(x) for x in actual_ser]) == sorted([str(x) for x in expected_ser]):
                            return True
                    except Exception:
                        pass

            return False

        # Step 4: Run testcases
        t0 = time.perf_counter()
        passed_count = 0
        case_results = []
        overall_status = 'Accepted'

        for idx, tc in enumerate(testcases):
            input_disp = tc.get('inputDisplay', '')
            exp_disp = tc.get('expectedDisplay', '')
            expected = tc.get('expected')

            try:
                if is_class:
                    methods = tc.get('methods', [])
                    method_args = tc.get('methodArgs', [])
                    obj = None
                    actual_outputs = []
                    for m, a in zip(methods, method_args):
                        if m == entry_fn or m == '__init__':
                            obj = target_class(*a)
                            actual_outputs.append(None)
                        else:
                            f = getattr(obj, m)
                            actual_outputs.append(f(*a))
                    actual_ser = serialize_res(actual_outputs)
                else:
                    args = tc.get('args', [])
                    if tc.get('hasLinkedList'):
                        args = [build_linked_list(a) if isinstance(a, list) and idx == 0 else a for idx, a in enumerate(args)]
                    elif tc.get('hasTree'):
                        args = [build_binary_tree(a) if isinstance(a, list) and idx == 0 else a for idx, a in enumerate(args)]
                    
                    # Try candidates if first returns None but expected is not None
                    actual = None
                    last_err = None
                    success_call = False
                    for fn in fn_candidates:
                        try:
                            res = invoke_candidate(fn, args)
                            if res is not None or expected is None or len(fn_candidates) == 1:
                                actual = res
                                success_call = True
                                break
                            actual = res
                        except Exception as ex:
                            last_err = ex

                    if not success_call and last_err is not None:
                        raise last_err

                    actual_ser = serialize_res(actual)

                expected_ser = serialize_res(expected)
                is_passed = check_is_passed(actual_ser, expected_ser, tc)

                if is_passed:
                    passed_count += 1
                else:
                    if overall_status == 'Accepted':
                        overall_status = 'Wrong Answer'

                case_results.append({
                    'caseIndex': idx + 1,
                    'passed': is_passed,
                    'inputDisplay': input_disp,
                    'expectedDisplay': exp_disp,
                    'actualDisplay': json.dumps(actual_ser)
                })
            except Exception as e:
                overall_status = 'Runtime Error'
                case_results.append({
                    'caseIndex': idx + 1,
                    'passed': False,
                    'inputDisplay': input_disp,
                    'expectedDisplay': exp_disp,
                    'actualDisplay': 'Error',
                    'error': traceback.format_exc()
                })
                break

        elapsed_ms = round((time.perf_counter() - t0) * 1000, 2)
        sys.stdout = old_stdout

        return {
            'status': overall_status,
            'runtimeMs': elapsed_ms,
            'passedCount': passed_count,
            'totalCount': len(testcases),
            'results': case_results,
            'stdout': stdout_buf.getvalue()
        }
    finally:
        sys.stdout = old_stdout

if __name__ == '__main__':
    raw = sys.stdin.read()
    if raw.strip():
        payload = json.loads(raw)
        res = run_payload(payload)
        print(json.dumps(res))
